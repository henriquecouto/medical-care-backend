from flask import jsonify, request, Blueprint
from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair
import json
from bson.objectid import ObjectId
from bson.json_util import dumps

from config.mongo import db
from utils.validate_keys import validate_keys

collection = db.attendance

attendanceApi = Blueprint('attendance-api', __name__)


@attendanceApi.route('/register', methods=['post'])
def register():

    data = request.get_json()

    keys = ['anamnesis', 'exams', 'patient', 'symptons']

    error = validate_keys(data, keys)

    if error:
        return error

    patient = db.patient.find_one({'_id': ObjectId(data['patient'])})

    if not patient:
        return jsonify({'result': 'patient not registered'})

    attendance = {'data': {}}

    for key in keys:
        if key == 'patient':
            attendance['data'][key] = patient['data']
        else:
            attendance['data'][key] = data[key]

    try:
        collection.insert_one(attendance)
        return jsonify({'result': 'success'})
    except:
        return jsonify({'result': 'an error ocurred'})

@attendanceApi.route('/', methods=['get'])
def getAttendances():
    try:
        attendances = json.loads(dumps(collection.find()))
        for attendance in attendances:
            attendance['_id'] = str(attendance['_id'])
        return jsonify({'result': attendances})
    except Exception as e:
        return jsonify({'result': 'an error ocurred'})
