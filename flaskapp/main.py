from flask import Flask, request, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient(os.environ['MONGO_URI'])
db = client.mydatabase

@app.route('/<key>', methods=['GET', 'POST', 'PUT'])
def key_value(key):
    if request.method == 'POST':
        value = request.json['value']
        db.keyvalue.insert_one({'key': key, 'value': value})
        return jsonify({'key': key, 'value': value}), 201

    elif request.method == 'PUT':
        value = request.json['value']
        db.keyvalue.update_one({'key': key}, {'$set': {'value': value}})
        return jsonify({'key': key, 'value': value})

    elif request.method == 'GET':
        document = db.keyvalue.find_one({'key': key})
        if document:
            return jsonify({'key': key, 'value': document['value']})
        else:
            return jsonify({'error': 'Key not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
