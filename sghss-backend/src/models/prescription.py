from src.models.user import db
from datetime import datetime

class Prescription(db.Model):
    __tablename__ = 'prescriptions'
    
    id = db.Column(db.Integer, primary_key=True)
    medical_record_id = db.Column(db.Integer, db.ForeignKey('medical_records.id'), nullable=False)
    medications = db.Column(db.JSON, nullable=False)  # JSON field for medications list
    instructions = db.Column(db.Text)
    valid_until = db.Column(db.Date)
    is_digital = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<Prescription {self.id} - MedicalRecord {self.medical_record_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'medical_record_id': self.medical_record_id,
            'medications': self.medications or [],
            'instructions': self.instructions,
            'valid_until': self.valid_until.isoformat() if self.valid_until else None,
            'is_digital': self.is_digital,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

