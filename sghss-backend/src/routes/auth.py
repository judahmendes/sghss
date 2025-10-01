from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, create_refresh_token
from src.models.user import db, User, UserRole
from src.models.patient import Patient
from src.models.professional import Professional
from src.utils import (
    validate_email,
    validate_password,
    validate_user_role,
    validate_required_fields,
    sanitize_string,
    create_response,
    get_current_user,
    log_user_action,
    ValidationError,
    AuthenticationError,
    AuthorizationError,
    NotFoundError,
    ConflictError,
    DatabaseError
)
from datetime import timedelta
import logging

auth_bp = Blueprint('auth', __name__)
logger = logging.getLogger('sghss')

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user with improved validation and error handling"""
    try:
        data = request.get_json()
        
        if not data:
            raise ValidationError("Request body is required")
        
        # Validate required fields
        is_valid, error_msg = validate_required_fields(data, ['email', 'password', 'role'])
        if not is_valid:
            raise ValidationError(error_msg)
        
        # Sanitize and validate email
        email = sanitize_string(data['email'].lower())
        if not validate_email(email):
            raise ValidationError("Invalid email format")
        
        # Validate password
        password = data['password']
        is_valid, error_msg = validate_password(password)
        if not is_valid:
            raise ValidationError(error_msg)
        
        # Validate role
        role = sanitize_string(data['role'].lower())
        if not validate_user_role(role):
            raise ValidationError("Invalid role. Must be patient, professional, or admin")
        
        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            raise ConflictError("Email already registered")
        
        # Create new user
        user = User(
            email=email,
            role=UserRole(role)
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        # Log user registration
        log_user_action(user.id, "USER_REGISTERED", f"New {role} user registered")
        
        return create_response(
            message="User registered successfully",
            data={'user': user.to_dict()},
            status_code=201
        )
        
    except (ValidationError, ConflictError) as e:
        return create_response(error=e.message, status_code=e.status_code)
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        db.session.rollback()
        return create_response(error="Registration failed", status_code=500)

@auth_bp.route('/login', methods=['POST'])
def login():
    """Authenticate user and return JWT tokens with improved security"""
    try:
        data = request.get_json()
        
        if not data:
            raise ValidationError("Request body is required")
        
        # Validate required fields
        is_valid, error_msg = validate_required_fields(data, ['email', 'password'])
        if not is_valid:
            raise ValidationError(error_msg)
        
        email = sanitize_string(data['email'].lower())
        password = data['password']
        
        # Validate email format
        if not validate_email(email):
            raise ValidationError("Invalid email format")
        
        # Find user
        user = User.query.filter_by(email=email).first()
        
        if not user or not user.check_password(password):
            # Log failed login attempt
            log_user_action(0, "LOGIN_FAILED", f"Failed login attempt for {email}")
            raise AuthenticationError("Invalid email or password")
        
        if not user.is_active:
            log_user_action(user.id, "LOGIN_BLOCKED", "Login attempt on deactivated account")
            raise AuthenticationError("Account is deactivated")
        
        # Create tokens
        access_token = create_access_token(
            identity=str(user.id),
            expires_delta=timedelta(hours=1)
        )
        refresh_token = create_refresh_token(
            identity=str(user.id),
            expires_delta=timedelta(days=30)
        )
        
        # Log successful login
        log_user_action(user.id, "LOGIN_SUCCESS", "User successfully logged in")
        
        return create_response(
            message="Login successful",
            data={
                'access_token': access_token,
                'refresh_token': refresh_token,
                'user': user.to_dict()
            }
        )
        
    except (ValidationError, AuthenticationError) as e:
        return create_response(error=e.message, status_code=e.status_code)
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return create_response(error="Login failed", status_code=500)

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Refresh access token with improved validation"""
    try:
        current_user_id = int(get_jwt_identity())
        user = User.query.get(current_user_id)
        
        if not user:
            raise NotFoundError("User not found")
        
        if not user.is_active:
            raise AuthenticationError("Account is deactivated")
        
        new_token = create_access_token(
            identity=str(current_user_id),
            expires_delta=timedelta(hours=1)
        )
        
        log_user_action(user.id, "TOKEN_REFRESHED", "Access token refreshed")
        
        return create_response(
            message="Token refreshed successfully",
            data={'access_token': new_token}
        )
        
    except (NotFoundError, AuthenticationError) as e:
        return create_response(error=e.message, status_code=e.status_code)
    except ValueError:
        return create_response(error="Invalid token", status_code=401)
    except Exception as e:
        logger.error(f"Token refresh error: {str(e)}")
        return create_response(error="Token refresh failed", status_code=500)


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user_info():
    """Get current user information with profile data"""
    try:
        user = get_current_user()
        
        user_data = user.to_dict()
        
        # Add profile data based on role
        if user.role == UserRole.PATIENT and user.patient:
            user_data['profile'] = user.patient.to_dict()
            user_data['profile']['age'] = user.patient.get_age()
        elif user.role == UserRole.PROFESSIONAL and user.professional:
            user_data['profile'] = user.professional.to_dict()
        
        return create_response(data={'user': user_data})
        
    except (AuthenticationError, NotFoundError) as e:
        return create_response(error=e.message, status_code=e.status_code)
    except Exception as e:
        logger.error(f"Get user info error: {str(e)}")
        return create_response(error="Failed to get user info", status_code=500)


@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """Logout user with audit logging"""
    try:
        user = get_current_user()
        log_user_action(user.id, "LOGOUT", "User logged out")
        
        return create_response(message="Logout successful")
        
    except Exception as e:
        logger.error(f"Logout error: {str(e)}")
        return create_response(message="Logout successful")  # Always return success for logout

