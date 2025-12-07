from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from app.models import User


class userserializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    username = serializers.CharField(validators=[
        UniqueValidator(
            queryset=User.objects.all(),
            message="El usuario no puede ser utilizado",
        )]
    )

    class Meta:
        model = User
        fields = ('id', 'name', 'last_name', 'username', 'email')
