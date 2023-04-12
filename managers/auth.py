from datetime import datetime, timedelta

import jwt
from decouple import config


class AuthManager:
    @staticmethod
    def encode_token(user):
        payload = {"sub": user.id, "exp": datetime.utcnow() + timedelta(days=2), "type": user.__class__.__name__}
        return jwt.encode(payload, key=config("JWT_SECRET"), algorithm="HS256")
