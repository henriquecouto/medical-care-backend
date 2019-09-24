from flask import jsonify, request, Blueprint
from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair
import json
from bson.objectid import ObjectId
from bson.json_util import dumps
from datetime import datetime

from config.mongo import db
from utils.validate_keys import validate_keys

from utils.transaction import scheduleTransaction

collection = db.attendance

attendanceApi = Blueprint('attendance-api', __name__)


@attendanceApi.route('/register', methods=['post'])
def register():

    data = request.get_json()
    keys = ['anamnese', 'exams', 'patient', 'symptoms', 'doctor']

    error = validate_keys(data, keys)

    if error:
        return error

    patient = db.patient.find_one({'_id': ObjectId(data['patient'])})
    doctor = db.doctor.find_one({'data.email': data['doctor']['user']})

    doctor['_id'] = str(doctor['_id'])

    data['doctor'] = doctor

    if not patient:
        return jsonify({'result': 'patient not registered'})

    attendance = {'data': {}}

    for key in keys:
        if key == 'patient':
            attendance['data'][key] = patient['data']
        else:
            attendance['data'][key] = data[key]

    attendance['data']['createdAt'] = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S.%f")

    try:
        obj = collection.insert_one(attendance)
        print(obj.inserted_id)
        scheduleTransaction(obj.inserted_id)
        return jsonify({'result': 'success'})
    except Exception as e:
        return jsonify({'result': 'an error ocurred oooo'})


@attendanceApi.route('/', methods=['get'])
def getAttendances():
    try:
        attendances = json.loads(dumps(collection.find()))

        return jsonify({'result': attendances})
    except Exception as e:
        return jsonify({'result': 'an error ocurred'})
