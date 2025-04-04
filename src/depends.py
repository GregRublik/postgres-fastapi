from repositories.repository import (
    UserRepository,
    )
from services import main, users, jwt_services


def users_service():
    return users.UserService(UserRepository)


def get_jwt_service():
    return jwt_services.JWTService()
