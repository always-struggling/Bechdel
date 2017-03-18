import json
from flask import Flask, jsonify, g, request
from flask_cors import CORS
from graph_data import Analyse


app = Flask(__name__)
CORS(app)

data = Analyse('data\\bechdel_data.json')


@app.route('/bechdel_buttons', methods=['GET'])
def get_buttons():
    """

    """
    button_data = data.get_button_json()
    return jsonify(button_data)

@app.route('/bechdel_scatter', methods=['POST'])
def get_scatter():
    """

    """
    x = json.loads(request.data.decode('utf-8'))['x']
    y = json.loads(request.data.decode('utf-8'))['y']
    r = json.loads(request.data.decode('utf-8'))['r']
    z = json.loads(request.data.decode('utf-8'))['z']
    scatter_data = data.get_scatter_json(x, y, r, z)
    return jsonify(scatter_data)


@app.route('/bechdel_bar', methods=['POST'])
def get_bar():
    """

    """
    x = json.loads(request.data.decode('utf-8'))['x']
    z = json.loads(request.data.decode('utf-8'))['z']
    y = json.loads(request.data.decode('utf-8'))['y']
    bar_data = data.get_bar_json(x, z, y)
    return jsonify(bar_data)