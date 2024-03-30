from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import os 

app = Flask(__name__) 
CORS(app)

@app.route('/api/data', methods=['GET']) 
@cross_origin()
def get_data():
    data = {'message': 'Hello from Python!'}
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
