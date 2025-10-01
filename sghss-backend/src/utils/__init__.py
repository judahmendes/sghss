"""
Utilitários do SGHSS Backend
"""

from .validators import (
    validate_email,
    validate_password,
    validate_cpf,
    validate_phone,
    validate_birth_date,
    validate_user_role,
    sanitize_string,
    validate_required_fields
)

from .exceptions import (
    SGHSSBaseException,
    ValidationError,
    AuthenticationError,
    AuthorizationError,
    NotFoundError,
    ConflictError,
    DatabaseError,
    BusinessLogicError
)

from .helpers import (
    setup_logging,
    create_response,
    require_role,
    get_current_user,
    paginate_query,
    format_cpf,
    format_phone,
    calculate_age,
    log_user_action,
    mask_sensitive_data
)

__all__ = [
    # Validators
    'validate_email',
    'validate_password', 
    'validate_cpf',
    'validate_phone',
    'validate_birth_date',
    'validate_user_role',
    'sanitize_string',
    'validate_required_fields',
    
    # Exceptions
    'SGHSSBaseException',
    'ValidationError',
    'AuthenticationError',
    'AuthorizationError',
    'NotFoundError',
    'ConflictError',
    'DatabaseError',
    'BusinessLogicError',
    
    # Helpers
    'setup_logging',
    'create_response',
    'require_role',
    'get_current_user',
    'paginate_query',
    'format_cpf',
    'format_phone',
    'calculate_age',
    'log_user_action',
    'mask_sensitive_data'
]
