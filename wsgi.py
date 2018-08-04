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


mongo = PyMongo(app)

token_obj = Token_use()


@application.route('/user', methods=['GET'])
def get_one_star():
    user = mongo.db.user
    token = request.args.get('token', type=str)
    output = []
    # s = star.find_one({'name' : name})
    for s in user.find({'token': token}):
        output.append({'name': s['name'], 'age': s['age'], 'pid': s['pid']})
    return jsonify({'result': output})


@application.route('/register', methods=['POST'])
def add_star():
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


if __name__ == '__main__':
    application.run(debug=True)
