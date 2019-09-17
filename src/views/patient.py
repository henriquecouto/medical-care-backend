from flask import jsonify, request, Blueprint
from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair
from pymongo import MongoClient
import json
from bson.json_util import dumps
from datetime import date
import re

from config.mongo import db
from utils.validate_keys import validate_keys

collection = db.patient

patientApi = Blueprint('patient-api', __name__)


@patientApi.route('/register', methods=['post'])
def register():
    data = request.get_json()

    keys = ['name', 'birthDate', 'gender', 'profession']

    error = validate_keys(data, keys)

    if error:
        return error

    patient = {'data': {}}

    for key in keys:
        patient['data'][key] = data[key]

    try:
        collection.insert_one(patient)
        return jsonify({'result': 'success'})
    except:
        return jsonify({'result': 'an error ocurred'})


@patientApi.route('/', methods=['get'])
def getPatients():
    try:
        patients = json.loads(dumps(collection.find()))

        return jsonify({'result': patients})
    except Exception as e:
        return jsonify({'result': 'an error ocurred'})


@patientApi.route('/search', methods=['post'])
def searchPatient():

    data = request.get_json()

    try:
        patient = json.loads(dumps(collection.find_one(
            {'data.name': re.compile('^' + data['name'] + '$', re.IGNORECASE)})))
        return jsonify({'result': patient})
    except Exception as e:
        return jsonify({'result': 'an error ocurred'})
