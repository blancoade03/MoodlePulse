import logging
import inspect
from functools import wraps

# Obtener logger específico para la API
logger = logging.getLogger('api')


class APILogger:
    """Clase helper para logging de API"""

    @staticmethod
    def log_request(request, view_name=None):
        """Log de peticiones entrantes"""
        user = request.user if request.user.is_authenticated else 'Anonymous'
        view = view_name or request.resolver_match.view_name if hasattr(request, 'resolver_match') else 'Unknown'

        log_data = {
            'user': str(user),
            'method': request.method,
            'path': request.path,
            'view': view,
            'ip': APILogger.get_client_ip(request),
            'user_agent': request.META.get('HTTP_USER_AGENT', ''),
        }

        logger.info(f"REQUEST | User: {log_data['user']} | "
                    f"Method: {log_data['method']} | "
                    f"Path: {log_data['path']} | "
                    f"IP: {log_data['ip']}")

        # Log body para POST/PUT/PATCH (excepto datos sensibles)
        if request.method in ['POST', 'PUT', 'PATCH'] and request.content_type == 'application/json':
            try:
                # Filtrar datos sensibles
                body = request.data.copy()
                sensitive_fields = ['password', 'token', 'secret', 'key', 'authorization']
                for field in sensitive_fields:
                    if field in body:
                        body[field] = '***REDACTED***'
                logger.debug(f"Request Body: {body}")
            except Exception:
                pass

        return log_data

    @staticmethod
    def log_response(request, response, view_name=None, duration=None):
        """Log de respuestas"""
        user = request.user if request.user.is_authenticated else 'Anonymous'
        view = view_name or request.resolver_match.view_name if hasattr(request, 'resolver_match') else 'Unknown'

        log_message = (f"RESPONSE | User: {user} | "
                       f"Method: {request.method} | "
                       f"Path: {request.path} | "
                       f"Status: {response.status_code}")

        if duration is not None:
            log_message += f" | Duration: {duration:.3f}s"

        if 200 <= response.status_code < 400:
            logger.info(log_message)
        elif 400 <= response.status_code < 500:
            logger.warning(log_message)
        else:
            logger.error(log_message)

        # Log error details
        if response.status_code >= 400 and hasattr(response, 'data'):
            logger.debug(f"Error details: {response.data}")

    @staticmethod
    def log_error(request, exception, view_name=None):
        """Log de excepciones"""
        user = request.user if request.user.is_authenticated else 'Anonymous'
        view = view_name or request.resolver_match.view_name if hasattr(request, 'resolver_match') else 'Unknown'

        logger.error(
            f"EXCEPTION | User: {user} | "
            f"Method: {request.method} | "
            f"Path: {request.path} | "
            f"Error: {type(exception).__name__} | "
            f"Message: {str(exception)}",
            exc_info=True
        )

    @staticmethod
    def log_activity(user, action, details=None):
        """Log de actividades específicas"""
        details_str = f" | Details: {details}" if details else ""
        logger.info(f"ACTIVITY | User: {user} | Action: {action}{details_str}")

    @staticmethod
    def get_client_ip(request):
        """Obtener IP del cliente"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


# Decorador para logging automático de vistas
def log_api_view(view_name=None):
    """Decorador para loggear automáticamente las vistas de API"""

    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            import time

            # Log de request
            APILogger.log_request(request, view_name)

            start_time = time.time()

            try:
                response = view_func(request, *args, **kwargs)
                duration = time.time() - start_time

                # Log de response
                APILogger.log_response(request, response, view_name, duration)

                return response
            except Exception as e:
                duration = time.time() - start_time
                APILogger.log_error(request, e, view_name)
                raise

        return wrapped_view

    return decorator