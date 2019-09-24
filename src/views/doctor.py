from flask import jsonify, request, Blueprint
from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair
from pymongo import MongoClient
import json
from bson.json_util import dumps
from datetime import date

from config.mongo import db
from utils.validate_keys import validate_keys

collection = db.doctor

doctorApi = Blueprint('doctor-api', __name__)


@doctorApi.route('/register', methods=['post'])
def register():
    data = request.get_json()

    keys = ['name', 'crm', 'specialty', 'email']

    error = validate_keys(data, keys)

    if error:
        return error

    doctor = {'data': {}}

    for key in keys:
        doctor['data'][key] = data[key]

    try:
        collection.insert_one(doctor)
        return jsonify({'result': 'success'})
    except:
        return jsonify({'result': 'an error ocurred'})


@doctorApi.route('/', methods=['get'])
def getDoctors():
    try:
        doctors = json.loads(dumps(collection.find()))
        for doctor in doctors:
            doctor['_id'] = str(doctor['_id'])
        return jsonify({'result': doctors})
    except Exception as e:
        return jsonify({'result': 'an error ocurred'})
