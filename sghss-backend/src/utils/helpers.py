"""
Utilitários gerais para o SGHSS Backend
"""
from typing import Dict, Any, Optional
from datetime import datetime, date, timedelta
import logging
import os
from functools import wraps
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity
from src.models.user import User
from src.utils.exceptions import AuthenticationError, AuthorizationError


def setup_logging() -> logging.Logger:
    """
    Configura logging para a aplicação
    
    Returns:
        logging.Logger: Logger configurado
    """
    # Criar diretório logs se não existir
    logs_dir = 'logs'
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/sghss.log'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger('sghss')


def create_response(
    message: str = None,
    data: Any = None,
    error: str = None,
    status_code: int = 200
) -> tuple:
    """
    Cria resposta padronizada da API
    
    Args:
        message (str): Mensagem de sucesso
        data (Any): Dados da resposta
        error (str): Mensagem de erro
        status_code (int): Código de status HTTP
    
    Returns:
        tuple: (response_dict, status_code)
    """
    response = {}
    
    if message:
        response['message'] = message
    
    if data is not None:
        if isinstance(data, dict):
            response.update(data)
        else:
            response['data'] = data
    
    if error:
        response['error'] = error
    
    return jsonify(response), status_code


def require_role(*allowed_roles):
    """
    Decorator para verificar roles de usuário
    
    Args:
        *allowed_roles: Roles permitidas
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                current_user_id = int(get_jwt_identity())
                user = User.query.get(current_user_id)
                
                if not user:
                    raise AuthenticationError("User not found")
                
                if not user.is_active:
                    raise AuthenticationError("Account is deactivated")
                
                if user.role.value not in allowed_roles:
                    raise AuthorizationError(f"Required role: {', '.join(allowed_roles)}")
                
                return f(*args, **kwargs)
                
            except ValueError:
                raise AuthenticationError("Invalid token")
                
        return decorated_function
    return decorator


def get_current_user() -> User:
    """
    Obtém usuário atual autenticado
    
    Returns:
        User: Usuário atual
        
    Raises:
        AuthenticationError: Se usuário não encontrado ou inativo
    """
    try:
        current_user_id = int(get_jwt_identity())
        user = User.query.get(current_user_id)
        
        if not user:
            raise AuthenticationError("User not found")
        
        if not user.is_active:
            raise AuthenticationError("Account is deactivated")
        
        return user
        
    except ValueError:
        raise AuthenticationError("Invalid token")


def paginate_query(query, page: int = 1, per_page: int = 20) -> Dict[str, Any]:
    """
    Pagina uma query do SQLAlchemy
    
    Args:
        query: Query do SQLAlchemy
        page (int): Número da página
        per_page (int): Items por página
    
    Returns:
        Dict[str, Any]: Dados paginados
    """
    if page < 1:
        page = 1
    
    if per_page < 1 or per_page > 100:
        per_page = 20
    
    paginated = query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )
    
    return {
        'items': [item.to_dict() if hasattr(item, 'to_dict') else item for item in paginated.items],
        'total': paginated.total,
        'pages': paginated.pages,
        'current_page': paginated.page,
        'per_page': paginated.per_page,
        'has_next': paginated.has_next,
        'has_prev': paginated.has_prev,
        'next_page': paginated.next_num if paginated.has_next else None,
        'prev_page': paginated.prev_num if paginated.has_prev else None
    }


def format_cpf(cpf: str) -> str:
    """
    Formata CPF para exibição
    
    Args:
        cpf (str): CPF sem formatação
    
    Returns:
        str: CPF formatado (XXX.XXX.XXX-XX)
    """
    if not cpf or len(cpf) != 11:
        return cpf
    
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"


def format_phone(phone: str) -> str:
    """
    Formata telefone para exibição
    
    Args:
        phone (str): Telefone sem formatação
    
    Returns:
        str: Telefone formatado
    """
    if not phone:
        return phone
    
    # Remove caracteres não numéricos
    digits = ''.join(filter(str.isdigit, phone))
    
    if len(digits) == 10:  # (XX) XXXX-XXXX
        return f"({digits[:2]}) {digits[2:6]}-{digits[6:]}"
    elif len(digits) == 11:  # (XX) 9XXXX-XXXX
        return f"({digits[:2]}) {digits[2:7]}-{digits[7:]}"
    
    return phone


def calculate_age(birth_date: date) -> Optional[int]:
    """
    Calcula idade baseada na data de nascimento
    
    Args:
        birth_date (date): Data de nascimento
    
    Returns:
        Optional[int]: Idade em anos
    """
    if not birth_date:
        return None
    
    today = date.today()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))


def log_user_action(user_id: int, action: str, details: str = None):
    """
    Registra ação do usuário para auditoria
    
    Args:
        user_id (int): ID do usuário
        action (str): Ação realizada
        details (str): Detalhes adicionais
    """
    logger = logging.getLogger('sghss')
    
    log_data = {
        'user_id': user_id,
        'action': action,
        'ip': request.remote_addr,
        'user_agent': request.headers.get('User-Agent'),
        'timestamp': datetime.utcnow().isoformat()
    }
    
    if details:
        log_data['details'] = details
    
    logger.info(f"User action: {log_data}")


def mask_sensitive_data(data: str, mask_char: str = '*', visible_chars: int = 4) -> str:
    """
    Mascara dados sensíveis
    
    Args:
        data (str): Dados a serem mascarados
        mask_char (str): Caractere para mascarar
        visible_chars (int): Caracteres visíveis no final
    
    Returns:
        str: Dados mascarados
    """
    if not data or len(data) <= visible_chars:
        return data
    
    masked_length = len(data) - visible_chars
    return mask_char * masked_length + data[-visible_chars:]
