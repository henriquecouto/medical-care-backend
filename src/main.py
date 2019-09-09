from flask import Flask
from views.patient import patientApi
from views.attendance import attendanceApi
from views.transaction import transactionApi


app = Flask(__name__)
app.register_blueprint(patientApi, url_prefix='/patient')
app.register_blueprint(attendanceApi, url_prefix='/attendance')
app.register_blueprint(transactionApi, url_prefix='/transaction')

if __name__ == '__main__':
    app.run(port=8000)
