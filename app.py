from flask import Flask, request, send_file, jsonify
from repository.database import db
from controllers.payment_controller import PaymentsController
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret_key_websocket"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)
socketio = SocketIO(app)

@app.route('/')
def index():
  controller = PaymentsController()
  return controller.home()

@app.route('/payments/pix', methods=['POST'])
def create_payment_pix():
  data = request.get_json()
  controller = PaymentsController()
  return controller.create_payment_pix(data)

@app.route('/payments/pix/qr_code/<file_name>', methods=['GET'])
def get_image(file_name):
    return send_file(f'static/img/{file_name}.png', mimetype='image/png')

@app.route('/payments/pix/confirmation', methods=['POST'])
def confirmation_page():
  controller = PaymentsController()  
  payment = controller.pix_confirmation()

  if isinstance(payment, tuple):  
    return payment  

  socketio.emit(f'payment-confirmed-{payment.id}', {'payment_id': payment.id})  
  return jsonify({"message": "The payment has been confirmed"})

@app.route('/payments/pix/<uuid:payment_id>', methods=['GET'])
def pix_page(payment_id):
  controller = PaymentsController()
  return controller.payment_pix_page(payment_id)

@socketio.on('connect')
def handle_connect():
  print("Client connected to the server")

@socketio.on('disconnect')
def handle_disconnect():
  print("Client has disconnected to the server")

if __name__ == '__main__':
  socketio.run(app, debug=True)