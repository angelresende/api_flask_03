from flask import jsonify, render_template, request 
from models.payment import Payment 
from datetime import datetime, timedelta
from repository.database import db
from payments.pix import Pix
from flask_socketio import emit

class PaymentsController:
  @staticmethod
  def home():
    return render_template('index.html')

  def create_payment_pix(self, data):

    if 'value' not in data:
      return jsonify({"message": "Invalid value"}), 400
    
    expiration_date = datetime.now() + timedelta(minutes=30)

    new_payment = Payment(value=data['value'],
                          expiration_date=expiration_date) 
    
    pix_obj = Pix()
    data_payment_pix = pix_obj.create_payment()    
    new_payment.bank_payment_id= data_payment_pix['bank_payment_id']
    new_payment.qr_code = data_payment_pix['qr_code_path']

    try:
      db.session.add(new_payment)
      db.session.commit()
      return jsonify({"message": "The payment has been created",
                      "payment": new_payment.to_dict()})
    
    except Exception as e:
      print(f"Error creating payment: {e}")
      return jsonify({"message": "Payment creation failed"}), 500   
  
  def pix_confirmation(self):
    data = request.get_json()

    if "bank_payment_id" not in data and "value" not in data:
      return jsonify({"message": "Invalid payment data"}), 400
    
    payment = Payment.query.filter_by(bank_payment_id=data.get("bank_payment_id")).first()

    if not payment:
      return jsonify({"message": "Payment not found"}), 404
    
    if data.get("value") != payment.value:
      return jsonify({"message": "Invalid payment data"}), 400
    
    payment.paid = True
    db.session.commit()   
    return payment
  
  @staticmethod
  def payment_pix_page(payment_id):
    try:
      payment = Payment.query.get(str(payment_id)) 

      if not payment:
        return render_template('404.html')

      if payment.paid:
        return render_template('confirmed_payment.html',
                                payment_id=payment.id,
                                value=payment.value
                              )
      
      return render_template('payment.html',
                              payment_id=payment.id,
                              value=payment.value,
                              host="http://127.0.0.1:5000/",
                              qr_code=payment.qr_code
                              )
      
              
    except Exception as e:
      return render_template('404.html', message=str(e))
    