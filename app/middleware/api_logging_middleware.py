import time
from django.utils.deprecation import MiddlewareMixin
from app.services.logger import APILogger


class APILoggingMiddleware(MiddlewareMixin):
    """Middleware para logging automático de todas las peticiones API"""

    def process_request(self, request):
        request.start_time = time.time()

        # Solo loggear peticiones a la API (ajusta según tu configuración)
        if request.path.startswith('/api/'):
            APILogger.log_request(request)

    def process_response(self, request, response):
        if hasattr(request, 'start_time') and request.path.startswith('/api/'):
            duration = time.time() - request.start_time
            APILogger.log_response(request, response, duration=duration)

        return response

    def process_exception(self, request, exception):
        if request.path.startswith('/api/'):
            APILogger.log_error(request, exception)
        return None