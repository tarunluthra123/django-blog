import jwt
from blog.config import Config


def encode(payload):
    return jwt.encode(payload, Config.JWT_SECRET)


def decode(token):
    return jwt.decode(token, Config.JWT_SECRET, algorithms=["HS256"])
