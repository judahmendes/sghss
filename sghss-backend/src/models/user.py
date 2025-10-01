from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import bcrypt
import enum

db = SQLAlchemy()

class UserRole(enum.Enum):
    PATIENT = "patient"
    PROFESSIONAL = "professional"
    ADMIN = "admin"

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum(UserRole), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    patient = db.relationship('Patient', backref='user', uselist=False, cascade='all, delete-orphan')
    professional = db.relationship('Professional', backref='user', uselist=False, cascade='all, delete-orphan')
    audit_logs = db.relationship('AuditLog', backref='user', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.email}>'

    def set_password(self, password: str) -> None:
        """
        Hash and set password with comprehensive validation
        
        Args:
            password (str): Plain text password
            
        Raises:
            ValueError: If password doesn't meet requirements
        """
        if not password or not isinstance(password, str):
            raise ValueError("Password is required and must be a string")
        
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        
        if len(password) > 128:
            raise ValueError("Password cannot exceed 128 characters")
        
        # Generate salt and hash password
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    def check_password(self, password: str) -> bool:
        """
        Check if provided password matches hash with safety checks
        
        Args:
            password (str): Plain text password to verify
            
        Returns:
            bool: True if password matches, False otherwise
        """
        if not password or not isinstance(password, str):
            return False
        
        if not self.password_hash:
            return False
        
        try:
            return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
        except (ValueError, TypeError):
            # Handle any bcrypt errors gracefully
            return False

    def is_patient(self) -> bool:
        """Check if user is a patient"""
        return self.role == UserRole.PATIENT
    
    def is_professional(self) -> bool:
        """Check if user is a professional"""
        return self.role == UserRole.PROFESSIONAL
    
    def is_admin(self) -> bool:
        """Check if user is an admin"""
        return self.role == UserRole.ADMIN
    
    def deactivate(self) -> None:
        """Deactivate user account"""
        self.is_active = False
    
    def activate(self) -> None:
        """Activate user account"""
        self.is_active = True
    
    def update_last_login(self) -> None:
        """Update last login timestamp"""
        self.updated_at = datetime.utcnow()
    
    @classmethod
    def find_by_email(cls, email: str):
        """Find user by email (case insensitive)"""
        if not email:
            return None
        return cls.query.filter_by(email=email.lower().strip()).first()
    
    def to_dict(self, include_sensitive: bool = False) -> dict:
        """
        Convert user to dictionary with optional sensitive data
        
        Args:
            include_sensitive (bool): Whether to include sensitive information
            
        Returns:
            dict: User data
        """
        data = {
            'id': self.id,
            'email': self.email,
            'role': self.role.value,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
        
        if include_sensitive:
            data['has_password'] = bool(self.password_hash)
            data['has_patient_profile'] = bool(self.patient)
            data['has_professional_profile'] = bool(self.professional)
        
        return data
