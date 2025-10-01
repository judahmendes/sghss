"""
Exceções customizadas para o SGHSS Backend
"""


class SGHSSBaseException(Exception):
    """Exceção base para o sistema SGHSS"""
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class ValidationError(SGHSSBaseException):
    """Exceção para erros de validação"""
    def __init__(self, message: str):
        super().__init__(message, 400)


class AuthenticationError(SGHSSBaseException):
    """Exceção para erros de autenticação"""
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, 401)


class AuthorizationError(SGHSSBaseException):
    """Exceção para erros de autorização"""
    def __init__(self, message: str = "Access denied"):
        super().__init__(message, 403)


class NotFoundError(SGHSSBaseException):
    """Exceção para recursos não encontrados"""
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, 404)


class ConflictError(SGHSSBaseException):
    """Exceção para conflitos de dados"""
    def __init__(self, message: str = "Data conflict"):
        super().__init__(message, 409)


class DatabaseError(SGHSSBaseException):
    """Exceção para erros de banco de dados"""
    def __init__(self, message: str = "Database operation failed"):
        super().__init__(message, 500)


class BusinessLogicError(SGHSSBaseException):
    """Exceção para erros de regra de negócio"""
    def __init__(self, message: str):
        super().__init__(message, 422)
