from flask import jsonify, Blueprint, request
from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair
from config.mongo import db
from bson.objectid import ObjectId
import json
from bson.json_util import dumps

baseUrl = 'http://localhost:9984'
# Criando objeto da classe BigChainDB

bdb = BigchainDB(baseUrl)
# Criando chaves privadas e públicas

key_consultation = generate_keypair()

attendances = db.attendance
transaction = db.transaction

transactionApi = Blueprint('transaction-api', __name__)


@transactionApi.route('/', methods=['get'])
def getTransactions():
    req = request.get_json()['search']
    finded = json.loads(dumps(bdb.transactions.get(asset_id=req)))

    return jsonify(finded)
