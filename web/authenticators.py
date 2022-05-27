from rest_framework import authentication
from web.models import User
from utils.jwt import decode
from jwt import DecodeError


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        jwt = request.headers.get("Authorization")

        if jwt:
            _, jwt = jwt.split(" ")
            try:
                payload = decode(jwt)
                user = User.objects.get(id=payload.get("id"))
                return (user, jwt)
            except (DecodeError, User.DoesNotExist):
                return None, None

        return None, None
