import bcrypt
from blog.config import Config


class Codec:
    def __init__(self, rounds=12):
        self.salt = bcrypt.gensalt(rounds)

    def encrypt(self, data):
        return bcrypt.hashpw(data.encode(), self.salt).decode()

    def compare(self, data, hashed):
        return bcrypt.checkpw(data.encode(), hashed.encode())


codec = Codec(Config.SALT_ROUNDS)
