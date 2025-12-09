from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class TokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['user'] = dict(
            username=user.username,
            name=user.first_name,
            last_name=user.last_name,
            rol=user.groups,
        )

        return token
