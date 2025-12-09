from rest_framework import viewsets, permissions
from app.models import User
from app.serializers.userserializer import userserializer


class userviewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = userserializer
    permission_classes = [permissions.IsAuthenticated]
