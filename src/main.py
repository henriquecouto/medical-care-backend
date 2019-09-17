from flask import Flask,  jsonify
from views.patient import patientApi
from views.attendance import attendanceApi
from views.transaction import transactionApi
from views.doctor import doctorApi
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/")
def helloWorld():
    return jsonify({'a': "Hello, cross-origin-world!"})


app.register_blueprint(patientApi, url_prefix='/patient')
app.register_blueprint(attendanceApi, url_prefix='/attendance')
app.register_blueprint(transactionApi, url_prefix='/transaction')
app.register_blueprint(doctorApi, url_prefix='/doctor')

if __name__ == '__main__':
    app.run(port=8000)
