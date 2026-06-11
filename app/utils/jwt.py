from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from app.config import settings

def create_access_token(data: dict) -> str:
    payload = data.copy()
    expiry = datetime.now(timezone.utc) + timedelta(minutes = settings.access_token_expire_minutes)

    payload["exp"] = expiry

    token = jwt.encode(
        payload,
        settings.secret_key,
        algorithm = settings.jwt_algorithm
    )

    return token