import json
from flask import Flask, jsonify, g, request
from flask_cors import CORS
from graph_data import Analyse


app = Flask(__name__)
CORS(app)

data = Analyse('data\\bechdel_data.json')

@app.route('/bechdel', methods=['GET'])
def get_scatter():
    """

    """
    scatter_data = data.get_scatter_json()
    return jsonify(scatter_data)


@app.route('/bechdel_bar', methods=['POST'])
def get_bar():
    """

    """
    field = json.loads(request.data.decode('utf-8'))['field']
    spread = json.loads(request.data.decode('utf-8'))['spread']
    bar_data = data.get_bar_json(field, spread)
    return jsonify(bar_data)