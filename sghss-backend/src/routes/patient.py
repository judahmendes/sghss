from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from src.models.user import db, User, UserRole
from src.models.patient import Patient
from src.utils import (
    validate_cpf,
    validate_phone,
    validate_birth_date,
    validate_required_fields,
    sanitize_string,
    create_response,
    get_current_user,
    require_role,
    log_user_action,
    format_cpf,
    format_phone,
    calculate_age,
    ValidationError,
    AuthenticationError,
    AuthorizationError,
    NotFoundError,
    ConflictError,
    BusinessLogicError
)
import logging

patient_bp = Blueprint('patient', __name__)
logger = logging.getLogger('sghss')

@patient_bp.route('/patients', methods=['POST'])
@jwt_required()
@require_role('patient')
def create_patient():
    """Create a new patient profile with improved validation"""
    try:
        user = get_current_user()
        
        # Check if user already has a patient profile
        if user.patient:
            raise BusinessLogicError("Patient profile already exists")
        
        data = request.get_json()
        if not data:
            raise ValidationError("Request body is required")
        
        # Validate required fields
        is_valid, error_msg = validate_required_fields(data, ['full_name', 'cpf', 'birth_date'])
        if not is_valid:
            raise ValidationError(error_msg)
        
        # Validate and sanitize data
        full_name = sanitize_string(data['full_name'], max_length=255)
        if not full_name:
            raise ValidationError("Full name cannot be empty")
        
        # Validate CPF
        cpf = data['cpf']
        if not validate_cpf(cpf):
            raise ValidationError("Invalid CPF format")
        
        # Remove formatting from CPF for storage
        clean_cpf = ''.join(filter(str.isdigit, cpf))
        
        # Check if CPF is already registered
        existing_patient = Patient.query.filter_by(cpf=clean_cpf).first()
        if existing_patient:
            raise ConflictError("CPF already registered")
        
        # Validate birth date
        is_valid, birth_date, error_msg = validate_birth_date(data['birth_date'])
        if not is_valid:
            raise ValidationError(error_msg)
        
        # Validate optional fields
        phone = data.get('phone')
        if phone and not validate_phone(phone):
            raise ValidationError("Invalid phone format")
        
        # Create patient
        patient = Patient(
            user_id=user.id,
            full_name=full_name,
            cpf=clean_cpf,
            birth_date=birth_date,
            phone=sanitize_string(phone) if phone else None,
            address=sanitize_string(data.get('address'), max_length=500) if data.get('address') else None,
            allergies=data.get('allergies', []),
            current_medications=data.get('current_medications', []),
            medical_history=sanitize_string(data.get('medical_history'), max_length=2000) if data.get('medical_history') else None
        )
        
        db.session.add(patient)
        db.session.commit()
        
        log_user_action(user.id, "PATIENT_PROFILE_CREATED", f"Patient profile created for {full_name}")
        
        # Prepare response with formatted data
        patient_data = patient.to_dict()
        patient_data['cpf'] = format_cpf(patient.cpf)
        patient_data['phone'] = format_phone(patient.phone) if patient.phone else None
        patient_data['age'] = calculate_age(patient.birth_date)
        
        return create_response(
            message="Patient profile created successfully",
            data={'patient': patient_data},
            status_code=201
        )
        
    except (ValidationError, ConflictError, BusinessLogicError, AuthenticationError) as e:
        return create_response(error=e.message, status_code=e.status_code)
    except Exception as e:
        logger.error(f"Create patient error: {str(e)}")
        db.session.rollback()
        return create_response(error="Failed to create patient profile", status_code=500)

@patient_bp.route('/patients/me', methods=['GET'])
@jwt_required()
@require_role('patient')
def get_my_patient_profile():
    """Get current user's patient profile with formatted data"""
    try:
        user = get_current_user()
        
        if not user.patient:
            raise NotFoundError("Patient profile not found")
        
        # Prepare response with formatted data
        patient_data = user.patient.to_dict()
        patient_data['cpf'] = format_cpf(user.patient.cpf)
        patient_data['phone'] = format_phone(user.patient.phone) if user.patient.phone else None
        patient_data['age'] = calculate_age(user.patient.birth_date)
        
        return create_response(data={'patient': patient_data})
        
    except (AuthenticationError, NotFoundError) as e:
        return create_response(error=e.message, status_code=e.status_code)
    except Exception as e:
        logger.error(f"Get patient profile error: {str(e)}")
        return create_response(error="Failed to get patient profile", status_code=500)


@patient_bp.route('/patients/me', methods=['PUT'])
@jwt_required()
@require_role('patient')
def update_my_patient_profile():
    """Update current user's patient profile with improved validation"""
    try:
        user = get_current_user()
        
        if not user.patient:
            raise NotFoundError("Patient profile not found")
        
        data = request.get_json()
        if not data:
            raise ValidationError("Request body is required")
        
        patient = user.patient
        
        # Update allowed fields with validation
        if 'full_name' in data:
            full_name = sanitize_string(data['full_name'], max_length=255)
            if not full_name:
                raise ValidationError("Full name cannot be empty")
            patient.full_name = full_name
        
        if 'phone' in data:
            phone = data['phone']
            if phone and not validate_phone(phone):
                raise ValidationError("Invalid phone format")
            patient.phone = sanitize_string(phone) if phone else None
        
        if 'address' in data:
            address = data['address']
            patient.address = sanitize_string(address, max_length=500) if address else None
        
        if 'allergies' in data:
            allergies = data['allergies']
            if not isinstance(allergies, list):
                raise ValidationError("Allergies must be a list")
            patient.allergies = allergies
        
        if 'current_medications' in data:
            medications = data['current_medications']
            if not isinstance(medications, list):
                raise ValidationError("Current medications must be a list")
            patient.current_medications = medications
        
        if 'medical_history' in data:
            history = data['medical_history']
            patient.medical_history = sanitize_string(history, max_length=2000) if history else None
        
        # Update birth_date if provided
        if 'birth_date' in data:
            is_valid, birth_date, error_msg = validate_birth_date(data['birth_date'])
            if not is_valid:
                raise ValidationError(error_msg)
            patient.birth_date = birth_date
        
        db.session.commit()
        
        log_user_action(user.id, "PATIENT_PROFILE_UPDATED", "Patient profile updated")
        
        # Prepare response with formatted data
        patient_data = patient.to_dict()
        patient_data['cpf'] = format_cpf(patient.cpf)
        patient_data['phone'] = format_phone(patient.phone) if patient.phone else None
        patient_data['age'] = calculate_age(patient.birth_date)
        
        return create_response(
            message="Patient profile updated successfully",
            data={'patient': patient_data}
        )
        
    except (ValidationError, AuthenticationError, NotFoundError) as e:
        return create_response(error=e.message, status_code=e.status_code)
    except Exception as e:
        logger.error(f"Update patient profile error: {str(e)}")
        db.session.rollback()
        return create_response(error="Failed to update patient profile", status_code=500)

@patient_bp.route('/patients', methods=['GET'])
@jwt_required()
@require_role('admin')  # Apenas administradores podem listar todos os pacientes
def list_patients():
    """List all patients (admin only)"""
    try:
        # Query parameters for pagination
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Limit per_page to prevent abuse
        per_page = min(per_page, 100)
        
        # Get patients with pagination
        patients_query = Patient.query.join(User).filter(User.is_active == True)
        patients_paginated = patients_query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        # Format patient data
        patients_data = []
        for patient in patients_paginated.items:
            patient_data = patient.to_dict()
            patient_data['cpf'] = format_cpf(patient.cpf)
            patient_data['phone'] = format_phone(patient.phone) if patient.phone else None
            patient_data['age'] = calculate_age(patient.birth_date)
            # Include user email for admin view
            patient_data['email'] = patient.user.email
            patients_data.append(patient_data)
        
        return create_response(
            data={
                'patients': patients_data,
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': patients_paginated.total,
                    'pages': patients_paginated.pages,
                    'has_next': patients_paginated.has_next,
                    'has_prev': patients_paginated.has_prev
                }
            }
        )
        
    except (AuthenticationError, AuthorizationError) as e:
        return create_response(error=e.message, status_code=e.status_code)
    except Exception as e:
        logger.error(f"List patients error: {str(e)}")
        return create_response(error="Failed to list patients", status_code=500)
