class ServiceNotFound(Exception):
    """Ошибка возникает когда сервис недоступен"""

    code = 500
    message = None

    def __init__(self, message: str = None):
        if message:
            self.message = message
        else:
            self.message = 'Ошибка в запросе'

    def __str__(self) -> str:
        return f'ServiceNotFound(msg={self.message})'


class Error4xx(Exception):
    """Базовый класс для всех ошибок 400"""


class Error400(Error4xx):
    """Ошибка в запросе"""

    code = 400
    message = None

    def __init__(self, message: str = None):
        if message:
            self.message = message
        else:
            self.message = 'Ошибка в запросе'

    def __str__(self) -> str:
        return f'Error400(msg={self.message})'


class Error401(Error4xx):
    """Ошибка говорит о том, что пользователь не авторизован"""

    code = 401
    message = None

    def __init__(self, message: str = None):
        if message:
            self.message = message
        else:
            self.message = 'Отказано в доступе'

    def __str__(self) -> str:
        return f'Error401(msg={self.message})'


class Error403(Error4xx):
    """Ошибка говорит о том, что токены неправильные"""

    code = 403
    message = None

    def __init__(self, message: str = None):
        if message:
            self.message = message
        else:
            self.message = 'Неверный токен авторизации'

    def __str__(self) -> str:
        return f'Error403(msg={self.message})'


class Error404(Error4xx):
    """Ошибка говорит о том, что неверный user_id"""

    code = 404
    message = None

    def __init__(self, message: str = None):
        if message:
            self.message = message
        else:
            self.message = 'Неверный user_id в запросе'

    def __str__(self) -> str:
        return f'Error404(msg={self.message})'


class Error405(Error4xx):
    """Ошибка говорит о том, что неверный user_id"""

    code = 405
    message = None

    def __init__(self, message: str = None):
        if message:
            self.message = message
        else:
            self.message = 'HTTP метод не подходит'

    def __str__(self) -> str:
        return f'Error404(msg={self.message})'

class Error422(Error4xx):
    """
    Ошибка говорит о том, что сервер не смог обработать
    содержащиеся в запросе инструкции
    (синтаксис запроса и content-type корректные)
    """

    code = 422
    message = None

    def __init__(self, message: str = None):
        if message:
            self.message = message
        else:
            self.message = 'Необрабатываемый контент'

    def __str__(self) -> str:
        return f'Error422(msg={self.message})'


class Error429(Error4xx):
    """
    Ошибка говорит о том, что превышем лимит запросов в минуту
    """

    code = 429
    message = None

    def __init__(self, message: str = None):
        if message:
            self.message = message
        else:
            self.message = 'Превышен time limit (rpm)'

    def __str__(self) -> str:
        return f'Error429(msg={self.message})'
