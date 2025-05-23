from fastapi import status, HTTPException


class MessagePublishException(BaseException):
    """Ошибка публикации сообщения в брокер"""


class MessageConsumeException(BaseException):
    """Ошибка потребления сообщения из брокера"""


class QueueEmptyException(BaseException):
    """Очередь пуста"""


class BrokerConnectionException(BaseException):
    """Ошибка подключения к брокеру"""


class ModelAlreadyExistsException(BaseException):
    pass


class ModelNoFoundException(BaseException):
    pass


class UserAlreadyExistsException(ModelAlreadyExistsException):
    pass


class UserNoFoundException(ModelNoFoundException):
    pass


class TokenExpiredException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail="Токен истек")


class TokenNoFoundException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail="Токен не найден")


PasswordMismatchException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Пароли не совпадают!'
)

IncorrectEmailOrPasswordException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Неверная почта или пароль'
)

NoJwtException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Токен не валидный!'
)

NoUserIdException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Не найден ID пользователя'
)

ForbiddenException = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail='Недостаточно прав!'
)
