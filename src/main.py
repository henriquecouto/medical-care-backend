from flask import Flask
from views.patient import patientApi
from views.attendance import attendanceApi
from views.transaction import transactionApi
from views.doctor import doctorApi


app = Flask(__name__)
app.register_blueprint(patientApi, url_prefix='/patient')
app.register_blueprint(attendanceApi, url_prefix='/attendance')
app.register_blueprint(transactionApi, url_prefix='/transaction')
app.register_blueprint(doctorApi, url_prefix='/doctor')

if __name__ == '__main__':
    app.run(port=8000)
