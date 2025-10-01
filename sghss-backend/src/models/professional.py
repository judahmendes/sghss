from src.models.user import db
from datetime import datetime

class Professional(db.Model):
    __tablename__ = 'professionals'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    full_name = db.Column(db.String(255), nullable=False)
    professional_id = db.Column(db.String(50), nullable=False)  # CRM, COREN, etc.
    specialty = db.Column(db.String(100), nullable=False)
    work_schedule = db.Column(db.JSON)  # JSON field for work schedule
    is_available = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    appointments = db.relationship('Appointment', backref='professional', lazy='dynamic')
    medical_records = db.relationship('MedicalRecord', backref='professional', lazy='dynamic')

    def __repr__(self):
        return f'<Professional {self.full_name} - {self.specialty}>'

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'full_name': self.full_name,
            'professional_id': self.professional_id,
            'specialty': self.specialty,
            'work_schedule': self.work_schedule or {},
            'is_available': self.is_available,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

