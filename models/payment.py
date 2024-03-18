import uuid
from repository.database import db

class Payment(db.Model):
  id = db.Column(db.String(200), primary_key=True, nullable=False, default=lambda: str(uuid.uuid4()))
  value = db.Column(db.Float)
  paid = db.Column(db.Boolean, default=False)
  bank_payment_id = db.Column(db.String(200), nullable=True)
  qr_code = db.Column(db.String(100), nullable=True)
  expiration_date = db.Column(db.DateTime)

  def to_dict(self):
    return {
      "id": str(uuid.uuid4()),
      "value": self.value,
      "paid": self.paid,
      "bank_payment_id": self.bank_payment_id,
      "qr_code": self.qr_code,
      "expiration_date": self.expiration_date      
    } 