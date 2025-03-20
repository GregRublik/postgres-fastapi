from schemas.users import UserCreate, UserLogin
from config import settings
import jwt
import bcrypt


class JWTService:

    # def __init__(self, repository: AbstractRepository):
    #     self.repository: AbstractRepository = repository()

    async def create_access(self, user: UserCreate | UserLogin):
        pass


async def encode_jwt(
    payload: dict,
    private_key: str = settings.jwt.private_key_path.read_text(),
    algorithm: str = settings.jwt.algorithm
):
    encoded = await jwt.encode(
        payload,
        private_key,
        algorithm=algorithm
    )
    return encoded


async def decode_jwt(
        token: str | bytes,
        public_key: str = settings.jwt.public_key_path.read_text(),
        algorithm: str = settings.jwt.algorithm
):
    decoded = await jwt.decode(
        token,
        public_key,
        algorithm=[algorithm]
    )
    return decoded


def hash_password(
        password: str
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
        hashed_password=hashed_password
    )
