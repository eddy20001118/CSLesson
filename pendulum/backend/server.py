from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from pendulum import PendulumSim
import math

app = Flask(__name__,
            static_folder="../dist/static",
            template_folder="../dist")
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
sim = PendulumSim()


@app.route('/api/res/pc', methods=['POST','GET'])
def res_pc():
    my_params = dict(request.json)
    for key in my_params:
        my_params[key] = float(my_params[key])

    print(my_params)
    sim.set_params(my_params)
    sim.reset_vars('pc')
    response = {
        'status': 200,
        'data': {
            'user_params': my_params,
            'res': sim.run()
        }
    }
    return jsonify(response)


@app.route('/api/res/rt')
def res_rt():
    index = int(request.args.get('index',0))
    my_params = dict(request.json)
    for key in my_params:
        my_params[key] = float(my_params[key])

    sim.set_params(my_params)
    if index == 0:
        sim.reset_vars('rt')
    response = {
        'status': 200,
        'data': {
            'user_params': my_params,
            'index': index,
            'res': sim.run_rt(index)
        }
    }
    return jsonify(response)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="127.0.0.1",port="5000")
