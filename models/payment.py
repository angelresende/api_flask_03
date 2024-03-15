from sqlalchemy import UUID
from repository.database import db

class Payment(db.Model):
  id = db.Column(UUID(as_uuid=True), primary_key=True, nullable=False)
  value = db.Column(db.Float)
  paid = db.Column(db.Boolean, default=False)
  bank_payment_id = db.Column(UUID(as_uuid=True), nullable=True)
  qr_code = db.Column(db.String(100), nullable=True)
  expiration_date = db.Column(db.DateTime)