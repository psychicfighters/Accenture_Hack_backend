from bson import ObjectId
from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
import urllib.parse
import sys

application = Flask(__name__)

application.config['MONGO_DBNAME'] = 'acc_comp_nik'
application.config['MONGO_URI'] = 'mongodb://nilagnik:' + urllib.parse.quote(
    "Nilu@1234") + '@ds113452.mlab.com:13452/acc_comp_nik'


# mongodb://<dbuser>:<dbpassword>@ds113452.mlab.com:13452/acc_comp_nik

class Token_use():
    token_user = 1010
    pid = 555

    def update(self):
        self.token_user = self.token_user + 1
        return self.token_user

    def new_pid(self):
        self.pid = self.pid + 1
        return self.pid

    def reset_evr(self):
        self.token_user = 1010
        self.pid = 555


mongo = PyMongo(application)

token_obj = Token_use()


@application.route('/reset', methods=['GET'])
def reset():
    token_obj.reset_evr()


@application.route('/user', methods=['GET'])
def get_user():
    user = mongo.db.user
    token = request.args.get('token', type=str)
    output = []
    # s = star.find_one({'name' : name})
    for s in user.find({'token': token}):
        output.append({'name': s['name'], 'age': s['age'], 'pid': s['pid']})

    if output is not None and len(output) != 0:
        error = False
    else:
        error = True

    return jsonify({'patientlist': output, 'error': error})


@application.route('/register', methods=['POST'])
def add_user():
    user = mongo.db.user
    name = request.json['name']
    age = request.json['age']
    addr = request.json['addr']
    try:
        token = request.json['token']
    except:
        token = str(token_obj.update())

    assign_pid = str(token_obj.new_pid())
    star_id = user.insert({'pid': assign_pid, 'token': token, 'name': name, 'age': age, 'addr': addr})
    # new_star = star.find_one({'_id': star_id })
    # output = {'name' : new_star['name'], 'distance' : new_star['distance']}
    #
    return jsonify({'pid': assign_pid, 'result_token': token})


@application.route('/checkuprequestlist', methods=['GET'])
def get_checkup_list():
    checkup = mongo.db.checkup
    pid = request.args.get('pid', type=str)
    output = []
    # s = star.find_one({'name' : name})
    for s in checkup.find({'pid': pid}):

        output.append({'id': str(s['_id']), 'timestamp': s['timestamp'], 'type': s['type'], 'status': s['status']})

    if output is not None and len(output) != 0:
        error = False
    else:
        error = True

    return jsonify({'checkupreqlist': output, 'error': error})


@application.route('/checkuprequest', methods=['POST'])
def request_checkup():
    checkup = mongo.db.checkup
    pid = request.json['pid']
    timestap = request.json['timestamp']
    type = request.json['type']

    check_id = checkup.insert({'pid': pid, 'timestamp': timestap, 'type': type, 'status': 'Pending'})
    return jsonify({'error': False})


@application.route('/checkupdone', methods=['POST'])
def checkup_update():
    checkup = mongo.db.checkup
    id = request.json['id']
    id = ObjectId(id)
    check_id = checkup.update_one({'_id': id}, {'$set': {'status': 'Done'}})
    return jsonify({'error': False})


@application.route('/prescriptionlist', method=['GET'])
def get_prescription_list():
    prescription = mongo.db.prescription
    pid = request.args.get('pid', type=str)
    output = []
    # s = star.find_one({'name' : name})
    for s in prescription.find({'pid': pid}):
        output.append({'id': str(s['_id']), 'timestamp': s['timestamp'], 'pid': s['type']})

    if output is not None and len(output) != 0:
        error = False
    else:
        error = True

    return jsonify({'prescriptionlist': output, 'error': error})


@application.route('/bplist', method=['GET'])
def get_bp_list():
    bp = mongo.db.bp
    pid = request.args.get('pid', type=str)
    output = []
    # s = star.find_one({'name' : name})
    for s in bp.find({'pid': pid}):
        output.append({'id': str(s['_id']), 'timestamp': s['timestamp'], 'sys': s['sys'], 'dia': s['dia']})

    if output is not None and len(output) != 0:
        error = False
    else:
        error = True

    return jsonify({'bplist': output, 'error': error})


@application.route('/sugarlist', method=['GET'])
def get_sugar_list():
    sugar = mongo.db.sugar
    pid = request.args.get('pid', type=str)
    output = []
    # s = star.find_one({'name' : name})
    for s in sugar.find({'pid': pid}):
        output.append({'id': str(s['_id']), 'timestamp': s['timestamp'], 'sugar_first': s['sugar_first'],
                       'sugar_pp': s['sugar_pp'], 'sugar_random': s['sugar_random']})

    if output is not None and len(output) != 0:
        error = False
    else:
        error = True

    return jsonify({'sugarlist': output, 'error': error})


@application.route('/vitallist', method=['GET'])
def get_vital_list():
    vitals = mongo.db.vitals
    pid = request.args.get('pid', type=str)
    output = []
    # s = star.find_one({'name' : name})
    for s in vitals.find({'pid': pid}):
        output.append({'id': str(s['_id']), 'timestamp': s['timestamp'], 'pid': s['pid']})

    if output is not None and len(output) != 0:
        error = False
    else:
        error = True

    return jsonify({'vitallist': output, 'error': error})


@application.route('/ecglist', method=['GET'])
def get_ecg_list():
    ecg = mongo.db.ecg
    pid = request.args.get('pid', type=str)
    output = []
    # s = star.find_one({'name' : name})
    for s in ecg.find({'pid': pid}):
        output.append({'id': str(s['_id']), 'timestamp': s['timestamp'], 'pid': s['type']})

    if output is not None and len(output) != 0:
        error = False
    else:
        error = True

    return jsonify({'ecglist': output, 'error': error})



if __name__ == '__main__':
    application.run(debug=True)
