import json
from flask import Flask, jsonify, g, request
from flask_cors import CORS
from graph_data import User


app = Flask(__name__)
CORS(app)





@app.route('/bechdel_start', methods=['POST'])
def get_start():
    """

    """
    type = json.loads(request.data.decode('utf-8'))['type']
    location = json.loads(request.data.decode('utf-8'))['location']
    user = User(location, type)
    print (user.df)
    metadata = user.get_metadata(user.df)
    return jsonify(metadata)

@app.route('/bechdel_scatter', methods=['POST'])
def get_scatter():
    """

    """
    x = json.loads(request.data.decode('utf-8'))['x']
    y = json.loads(request.data.decode('utf-8'))['y']
    z = json.loads(request.data.decode('utf-8'))['z']
    scatter_data = 5#user.get_scatter_json(x, y, z)
    return jsonify(scatter_data)


@app.route('/bechdel_bar', methods=['POST'])
def get_bar():
    """

    """
    x = json.loads(request.data.decode('utf-8'))['x']
    z = json.loads(request.data.decode('utf-8'))['z']
    y = json.loads(request.data.decode('utf-8'))['y']
    bar_data = 5#data.get_bar_json(x, z, y)
    return jsonify(bar_data)