from bson import ObjectId
from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
import urllib.parse
import diab_prediction
import sys

application = Flask(__name__)

application.config['MONGO_DBNAME'] = 'acc_comp_nik'
application.config['MONGO_URI'] = ''


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
    return jsonify({"hola": "hola"})


@application.route('/user', methods=['GET'])     #done
def get_user():
    user = mongo.db.user
    token = request.args.get('token', type=str)
    output = []

    for s in user.find({'token': token}):
        output.append({'name': s['name'], 'age': s['age'], 'pid': s['pid']})

    if output is not None and len(output) != 0:
        error = False
    else:
        error = True

    return jsonify({'patientlist': output, 'error': error})


@application.route('/register', methods=['POST'])    #done
def add_user():
    user = mongo.db.user
    name = request.json['name']
    age = request.json['age']
    addr = request.json['addr']
    email = request.json['email']
    gender = request.json['gender']
    user_count = mongo.db.usercount
    try:
        token = request.json['token']
        if len(token) == 0:
            raise Exception('')
    except:


        val = user_count.find_one({})
        try:
            if val['count'] is None or val['count'] == 0:
                pass
        except:
            id = user_count.insert({'count': 11007, 'pcount': 7643})
            #else:

        try:
            id = user_count.update_one({}, {'$set': {'count': val['count'] + 1}})
        except:
            pass
        val = user_count.find_one({})
        token = str(val['count'])

    val = user_count.find_one({})
    id = user_count.update_one({}, {'$set': {'pcount': val['pcount'] + 1}})
    assign_pid = 'PA' + str(val['pcount'])
    star_id = user.insert({'pid': assign_pid, 'token': token, 'name': name, 'age': age, 'addr': addr, 'email': email,
                           'gender': gender})

    return jsonify({'pid': assign_pid, 'result_token': token})


@application.route('/checkuprequestlist', methods=['GET'])  #done
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


@application.route('/checkuprequest', methods=['POST'])     #done
def request_checkup():
    checkup = mongo.db.checkup
    pid = request.json['pid']
    timestap = request.json['timestamp']
    type = request.json['type']

    check_id = checkup.insert({'pid': pid, 'timestamp': timestap, 'type': type, 'status': 'Pending'})
    return jsonify({'error': False})


@application.route('/checkupdone', methods=['POST'])        #done
def checkup_update():
    checkup = mongo.db.checkup
    id = request.json['id']
    id = ObjectId(id)
    check_id = checkup.update_one({'_id': id}, {'$set': {'status': 'Done'}})
    return jsonify({'error': False})


@application.route('/prescriptionlist', methods=['GET'])    #done
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


@application.route('/presimage', methods=['GET'])           #done
def get_pres_image():
    prescription = mongo.db.prescription
    id = request.args.get('id', type=str)
    output = []
    id = ObjectId(id)
    # s = star.find_one({'name' : name})
    s = prescription.find_one({'_id': id})

    return jsonify({'prescription_image': s['prescription_image'], 'timestamp': s['timestamp'], 'error': False})


@application.route('/uploadpres', methods=['POST'])         #done
def upload_prescription():
    prescription = mongo.db.prescription
    pid = request.json['pid']
    timestamp = request.json['timestamp']
    url = request.json['url']
    type = request.json['type']
    check_id = prescription.insert({'pid': pid, 'timestamp': timestamp, 'prescription_image': url, 'type': type})
    return jsonify({'error': False})


@application.route('/ecglist', methods=['GET'])         #done
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


@application.route('/ecgimage', methods=['GET'])        #done
def get_ecg_image():
    ecg = mongo.db.ecg
    id = request.args.get('id', type=str)
    output = []
    # s = star.find_one({'name' : name})
    s = ecg.find_one({'_id': ObjectId(id)})

    return jsonify({'timestamp': s['timestamp'], 'ecg_url': s['ecg_url'], 'error': False})


@application.route('/uploadecg', methods=['POST'])      #done
def upload_ecg():
    ecg = mongo.db.ecg
    pid = request.json['pid']
    timestamp = request.json['timestamp']
    url = request.json['url']
    type = request.json['type']
    check_id = ecg.insert({'pid': pid, 'timestamp': timestamp, 'ecg_url': url, 'type': type})
    return jsonify({'error': False})


@application.route('/bplist', methods=['GET'])      #done
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


@application.route('/bpupload', methods=['POST'])       #done
def upload_bp():
    bp = mongo.db.bp
    pid = request.json['pid']
    timestamp = request.json['timestamp']
    sys = request.json['sys']
    dia = request.json['dia']
    check_id = bp.insert({'pid': pid, 'timestamp': timestamp, 'sys': sys, 'dia': dia})
    return jsonify({'error': False})


@application.route('/sugarlist', methods=['GET'])       #done
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


@application.route('/uploadsugar', methods=['POST'])    #done
def upload_sugar():
    sugar = mongo.db.sugar
    pid = request.json['pid']
    timestamp = request.json['timestamp']
    sugar_first = request.json['sugar_first']
    sugar_pp = request.json['sugar_pp']
    sugar_random = request.json['sugar_random']
    check_id = sugar.insert({'pid': pid, 'timestamp': timestamp, 'sugar_first': sugar_first, 'sugar_pp': sugar_pp,
                             'sugar_random': sugar_random})
    return jsonify({'error': False})


@application.route('/vitallist', methods=['GET'])       #done
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


@application.route('/vitaldetails', methods=['GET'])    #done
def get_vital_detail_list():
    vital = mongo.db.vitals
    pid = request.args.get('pid', type=str)
    timestamp = request.args.get('timestamp', type=str)
    output = []
    # s = star.find_one({'name' : name})
    for s in vital.find({'pid': pid, 'timestamp': timestamp}):
        output.append({'id': str(s['_id']), 'type': s['type'], 'value': s['value']})

    if output is not None and len(output) != 0:
        error = False
    else:
        error = True

    return jsonify({'vitaldetails': output, 'error': error})


@application.route('/uploadvitals', methods=['POST'])      #done
def upload_vitals():
    vital = mongo.db.vitals
    pid = request.json['pid']
    type = request.json['type']
    value = request.json['value']
    timestamp = request.json['timestamp']
    check_id = vital.insert({'pid': pid, 'timestamp': timestamp, 'type': type, 'value': value})
    return jsonify({'error': False})

@application.route('/calculatesugar', methods=['GET'])
def calculatesugar():
    #Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age, Outcome will show in this section
    glucose = request.args.get('glucose', type=str)
    pressure = request.args.get('pressure', type=str)
    bmi = request.args.get('bmi', type=str)
    age = request.args.get('age', type=str)
    list = [0, glucose, pressure, bmi, age]
    pred = diab_prediction.get(list)
    return jsonify({'probability': str(pred[0])})

if __name__ == '__main__':
    application.run(debug=False)
