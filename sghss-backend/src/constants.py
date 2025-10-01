"""
Configurações e constraints do banco de dados para o SGHSS
"""

# Constraints de tamanho para campos de texto
FIELD_LENGTHS = {
    'email': 255,
    'password_hash': 255,
    'full_name': 255,
    'cpf': 11,
    'phone': 20,
    'address': 500,
    'medical_history': 2000,
    'professional_id': 50,
    'specialty': 100,
    'diagnosis': 1000,
    'treatment': 1000,
    'observations': 1000,
    'instructions': 1000
}

# Valores padrão
DEFAULTS = {
    'is_active': True,
    'is_available': True,
    'is_digital': True,
    'allergies': [],
    'current_medications': [],
    'work_schedule': {}
}

# Constraints de validação
VALIDATION_RULES = {
    'password_min_length': 8,
    'password_max_length': 128,
    'cpf_length': 11,
    'phone_min_length': 10,
    'phone_max_length': 11,
    'max_age': 120,
    'token_expiry_hours': 1,
    'refresh_token_expiry_days': 30
}

# Enums válidos
VALID_USER_ROLES = ['patient', 'professional', 'admin']
VALID_APPOINTMENT_TYPES = ['presencial', 'telemedicina']
VALID_APPOINTMENT_STATUS = ['agendada', 'realizada', 'cancelada']

# Configurações de auditoria
AUDIT_ACTIONS = {
    'USER_REGISTERED': 'User registration',
    'LOGIN_SUCCESS': 'Successful login',
    'LOGIN_FAILED': 'Failed login attempt',
    'LOGIN_BLOCKED': 'Login blocked - inactive account',
    'LOGOUT': 'User logout',
    'TOKEN_REFRESHED': 'Token refreshed',
    'PATIENT_PROFILE_CREATED': 'Patient profile created',
    'PATIENT_PROFILE_UPDATED': 'Patient profile updated',
    'PROFESSIONAL_PROFILE_CREATED': 'Professional profile created',
    'PROFESSIONAL_PROFILE_UPDATED': 'Professional profile updated',
    'APPOINTMENT_CREATED': 'Appointment created',
    'APPOINTMENT_UPDATED': 'Appointment updated',
    'APPOINTMENT_CANCELLED': 'Appointment cancelled',
    'MEDICAL_RECORD_CREATED': 'Medical record created',
    'MEDICAL_RECORD_UPDATED': 'Medical record updated',
    'PRESCRIPTION_CREATED': 'Prescription created',
    'PRESCRIPTION_UPDATED': 'Prescription updated'
}

# Configurações de paginação
PAGINATION = {
    'default_per_page': 20,
    'max_per_page': 100,
    'min_per_page': 1
}

# Configurações de log
LOG_LEVELS = {
    'development': 'DEBUG',
    'testing': 'INFO',
    'production': 'WARNING'
}

# Configurações de segurança
SECURITY = {
    'max_login_attempts': 5,
    'lockout_duration_minutes': 30,
    'password_history_count': 5,
    'session_timeout_minutes': 60
}
