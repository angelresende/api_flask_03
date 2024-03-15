from flask import Flask, jsonify
from repository.database import db
from models.payment import Payment

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret_key_websocket"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)

@app.route('/payments/pix', methods=['POST'])
def create_payment_pix():
  return jsonify({"message": "The payment has been created"})

@app.route('/payments/pix/confirmation', methods=['POST'])
def pix_confimation():
  return jsonify({"message": "The payment has been confirmed"})

@app.route('/payments/pix/<uuid:payment_id>', methods=['GET'])
def payment_pix_page():
  return jsonify({"message": "Pix payment"})

if __name__ == '__main__':
  app.run(debug=True)