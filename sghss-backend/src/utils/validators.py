"""
Módulo de validadores para o SGHSS Backend
Contém funções de validação reutilizáveis
"""
import re
from typing import Tuple, Optional
from datetime import datetime, date


def validate_email(email: str) -> bool:
    """
    Valida formato de email
    
    Args:
        email (str): Email a ser validado
    
    Returns:
        bool: True se válido, False caso contrário
    """
    if not email or not isinstance(email, str):
        return False
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email.strip()) is not None


def validate_password(password: str) -> Tuple[bool, str]:
    """
    Valida força da senha
    
    Args:
        password (str): Senha a ser validada
    
    Returns:
        Tuple[bool, str]: (é_válida, mensagem)
    """
    if not password or not isinstance(password, str):
        return False, "Password is required"
    
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not re.search(r'[A-Za-z]', password):
        return False, "Password must contain at least one letter"
    
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character"
    
    return True, "Password is valid"


def validate_cpf(cpf: str) -> bool:
    """
    Valida CPF brasileiro (com verificação dos dígitos)
    
    Args:
        cpf (str): CPF a ser validado
    
    Returns:
        bool: True se válido, False caso contrário
    """
    if not cpf or not isinstance(cpf, str):
        return False
    
    # Remove caracteres não numéricos
    cpf = re.sub(r'[^0-9]', '', cpf)
    
    # Verifica se tem 11 dígitos
    if len(cpf) != 11:
        return False
    
    # Verifica se todos os dígitos são iguais (CPF inválido)
    if cpf == cpf[0] * 11:
        return False
    
    # Validação dos dígitos verificadores
    def calculate_digit(cpf_digits: str, weights: list) -> int:
        total = sum(int(digit) * weight for digit, weight in zip(cpf_digits, weights))
        remainder = total % 11
        return 0 if remainder < 2 else 11 - remainder
    
    # Primeiro dígito verificador
    first_digit = calculate_digit(cpf[:9], list(range(10, 1, -1)))
    if int(cpf[9]) != first_digit:
        return False
    
    # Segundo dígito verificador
    second_digit = calculate_digit(cpf[:10], list(range(11, 1, -1)))
    if int(cpf[10]) != second_digit:
        return False
    
    return True


def validate_phone(phone: str) -> bool:
    """
    Valida formato de telefone brasileiro
    
    Args:
        phone (str): Telefone a ser validado
    
    Returns:
        bool: True se válido, False caso contrário
    """
    if not phone or not isinstance(phone, str):
        return False
    
    # Remove caracteres não numéricos
    phone_digits = re.sub(r'[^0-9]', '', phone)
    
    # Verifica se tem 10 ou 11 dígitos (com DDD)
    return len(phone_digits) in [10, 11]


def validate_birth_date(birth_date_str: str) -> Tuple[bool, Optional[date], str]:
    """
    Valida e converte data de nascimento
    
    Args:
        birth_date_str (str): Data no formato YYYY-MM-DD
    
    Returns:
        Tuple[bool, Optional[date], str]: (é_válida, data_convertida, mensagem)
    """
    if not birth_date_str or not isinstance(birth_date_str, str):
        return False, None, "Birth date is required"
    
    try:
        birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date()
        
        # Verifica se a data não é no futuro
        if birth_date > date.today():
            return False, None, "Birth date cannot be in the future"
        
        # Verifica se a idade é razoável (máximo 120 anos)
        today = date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        
        if age > 120:
            return False, None, "Invalid birth date: age cannot exceed 120 years"
        
        return True, birth_date, "Valid birth date"
        
    except ValueError:
        return False, None, "Invalid birth date format. Use YYYY-MM-DD"


def validate_user_role(role: str) -> bool:
    """
    Valida role de usuário
    
    Args:
        role (str): Role a ser validada
    
    Returns:
        bool: True se válida, False caso contrário
    """
    if not role or not isinstance(role, str):
        return False
    
    valid_roles = ['patient', 'professional', 'admin']
    return role.lower().strip() in valid_roles


def sanitize_string(text: str, max_length: Optional[int] = None) -> str:
    """
    Sanitiza string removendo espaços extras e limitando tamanho
    
    Args:
        text (str): Texto a ser sanitizado
        max_length (Optional[int]): Tamanho máximo
    
    Returns:
        str: Texto sanitizado
    """
    if not text or not isinstance(text, str):
        return ""
    
    # Remove espaços extras
    sanitized = re.sub(r'\s+', ' ', text.strip())
    
    # Limita tamanho se especificado
    if max_length and len(sanitized) > max_length:
        sanitized = sanitized[:max_length]
    
    return sanitized


def validate_required_fields(data: dict, required_fields: list) -> Tuple[bool, str]:
    """
    Valida se todos os campos obrigatórios estão presentes
    
    Args:
        data (dict): Dados a serem validados
        required_fields (list): Lista de campos obrigatórios
    
    Returns:
        Tuple[bool, str]: (são_válidos, mensagem_erro)
    """
    if not isinstance(data, dict):
        return False, "Invalid data format"
    
    missing_fields = []
    for field in required_fields:
        if field not in data or data[field] is None or str(data[field]).strip() == "":
            missing_fields.append(field)
    
    if missing_fields:
        return False, f"Missing required fields: {', '.join(missing_fields)}"
    
    return True, "All required fields present"
