from src.models.user import db
from datetime import datetime
import enum

class AppointmentType(enum.Enum):
    PRESENCIAL = "presencial"
    TELEMEDICINA = "telemedicina"

class AppointmentStatus(enum.Enum):
    AGENDADA = "agendada"
    REALIZADA = "realizada"
    CANCELADA = "cancelada"

class Appointment(db.Model):
    __tablename__ = 'appointments'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('professionals.id'), nullable=False)
    appointment_date = db.Column(db.DateTime, nullable=False)
    appointment_type = db.Column(db.Enum(AppointmentType), nullable=False)
    status = db.Column(db.Enum(AppointmentStatus), default=AppointmentStatus.AGENDADA, nullable=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    medical_record = db.relationship('MedicalRecord', backref='appointment', uselist=False)

    def __repr__(self):
        return f'<Appointment {self.id} - {self.appointment_date}>'

    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'professional_id': self.professional_id,
            'appointment_date': self.appointment_date.isoformat(),
            'appointment_type': self.appointment_type.value,
            'status': self.status.value,
            'notes': self.notes,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

