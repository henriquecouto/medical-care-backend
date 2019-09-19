from flask import jsonify, Blueprint, request
from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair
from config.mongo import db
from bson.objectid import ObjectId
import json
from bson.json_util import dumps
import threading

baseUrl = 'http://localhost:9984'
# Criando objeto da classe BigChainDB

bdb = BigchainDB(baseUrl)
# Criando chaves privadas e públicas

key_consultation = generate_keypair()

attendances = db.attendance
transaction = db.transaction


def makeTransaction(attendance_id):
    print('Transactioning attendance: '+attendance_id)
    obj = dumps(attendances.find_one({'_id': ObjectId(attendance_id)}))

    attendance = json.loads(obj)

    attendance['_id'] = str(attendance['_id'])

    medical_consultation = {
        'data': {
            'medical_consultation': attendance,
        }
    }

    # Preparando a transação
    prepared_creation_tx = bdb.transactions.prepare(
        operation='CREATE',
        signers=key_consultation.public_key,
        asset=medical_consultation,
    )

    # Assinando transação com a chave privada
    fulfilled_creation_tx = bdb.transactions.fulfill(
        prepared_creation_tx, private_keys=key_consultation.private_key
    )

    # Enviando para o nó do BigChainDB
    sent_creation_tx = bdb.transactions.send_commit(fulfilled_creation_tx)

    # Verificando se a transação assinada é identica a submetida na rede
    if not sent_creation_tx == fulfilled_creation_tx:
        print("Error entering data")

    # Pegando identificador da transação
    block_id = fulfilled_creation_tx['id']

    transaction.insert_one({
        "transaction_id": block_id,
        # "user_id": req['user']
    })

    print({
        "block_id": block_id,
        "attendance": sent_creation_tx['asset']['data']['medical_consultation'],
        "message": "created"
    })


def scheduleTransaction(attendance_id):
    def job():
        makeTransaction(str(attendance_id))

    timer = threading.Timer(172800.0, job)
    timer.start()
