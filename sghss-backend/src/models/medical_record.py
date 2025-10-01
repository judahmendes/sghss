from src.models.user import db
from datetime import datetime

class MedicalRecord(db.Model):
    __tablename__ = 'medical_records'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('professionals.id'), nullable=False)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id'), nullable=True)
    diagnosis = db.Column(db.Text)
    treatment = db.Column(db.Text)
    observations = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    prescriptions = db.relationship('Prescription', backref='medical_record', lazy='dynamic')

    def __repr__(self):
        return f'<MedicalRecord {self.id} - Patient {self.patient_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'professional_id': self.professional_id,
            'appointment_id': self.appointment_id,
            'diagnosis': self.diagnosis,
            'treatment': self.treatment,
            'observations': self.observations,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

