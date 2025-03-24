from datetime import datetime, timedelta
from typing import Optional, Dict, Any

from config import settings
import jwt
import bcrypt

from schemas.users import UserCreate, UserLogin


async def encode_jwt(
        payload: Dict[str, Any],
        private_key: str = settings.jwt.private_key_path.read_text(),
        algorithm: str = settings.jwt.algorithm,
        expire_minutes: int = settings.jwt.access_token_expire_minutes,
        expire_timedelta: Optional[timedelta] = None,
) -> str:
    to_encode = payload.copy()
    now = datetime.utcnow()

    expire = (
        now + expire_timedelta
        if expire_timedelta
        else now + timedelta(minutes=expire_minutes)
    )

    to_encode.update(
        exp=expire,
        iat=now,
    )

    encoded = jwt.encode(
        to_encode,
        private_key,
        algorithm=algorithm,
    )

    return encoded


def decode_jwt(
    token: str | bytes,
    public_key: str = settings.jwt.public_key_path.read_text(),
    algorithm: str = settings.jwt.algorithm,
) -> dict:
    decoded = jwt.decode(
        token,
        public_key,
        algorithms=[algorithm],
    )
    return decoded


def hash_password(
    password: str,
) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


def validate_password(
    password: str,
    hashed_password: bytes,
) -> bool:
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password,
    )


class JWTService:

    # def __init__(self, repository: AbstractRepository):
    #     self.repository: AbstractRepository = repository()

    async def create_access_token(self, user: UserCreate | UserLogin):
        jwt_payload = {
            "sub": user.email,
        }
        return await encode_jwt(jwt_payload)

