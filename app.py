import os
import json
from dotenv import load_dotenv
from flask import Flask, request 
from pymongo import MongoClient
from bson import ObjectId, json_util
from datetime import datetime

load_dotenv()

application_root = os.getenv("application_root")
mongodb_url = os.getenv("mongodb_url")
app = Flask(__name__)

client = MongoClient(mongodb_url)
db = client['python-flask-mongodb-backend']
collection = db['data']

@app.route(application_root + '/', methods=["GET"])
def index():
    return {
        "status": "ok",
        "message": "",
        "version": 1.0
    }, 200

@app.route(application_root + '/todos/', methods=["GET"])
def read():
    #     
    data = collection.find({})
    todos = list(data)
    todosJson = json.loads(json_util.dumps(todos))
    return {
        "status": "ok",
        "message": "",
        "data": todosJson
    }, 200

@app.route(application_root + '/todos/<id>', methods=["GET"])
def read_one_by_id(id):
    
    filter = {
        "_id": ObjectId(id)
    }

    data = collection.find_one(filter)
    todosJson = json.loads(json_util.dumps(data))
    return {
        "status": "ok",
        "message": "",
        "data": todosJson
    }, 200

@app.route(application_root + '/todos/<id>', methods=["PUT"])
def update_one_by_id(id):
    
    data = request.json
    print(data)
    filter = {
        "_id": ObjectId(id)
    }

    payload = {}
    payload.update({"$set": {}})

    curDate = datetime.now().isoformat()

    if 'title' in data:
        payload["$set"].update({'title': data['title']})

    if 'description' in data:
        payload["$set"].update({'description': data['description']})

    if 'title' in data or 'decription' in data:
        payload["$set"].update({'meta.modifiedAt': curDate})

    data = collection.update_one(filter, payload, upsert=False)
    return {
        "status": "ok",
        "message": "Document with ID " + id + " successfully updated."
    }, 200

@app.route(application_root + '/todos/', methods=["POST"])
def create_one():
    data = request.json
    collection.insert_one(data)
    return {
        "status": "ok",
        "message": ""
    }, 201

@app.route(application_root + '/todos/<id>', methods=["DELETE"])
def delete_one_by_id(id):
    filter = {
        "_id": ObjectId(id)
    }
    res = collection.delete_one(filter)
    if res.deleted_count == 1:
        return {
            "status": "ok",
            "message": "Document with ID " + id + " deleted successfully."
        }, 200
    else:
        return {
            "status": "not found",
            "message": "Document with ID " + id + " not found."
        }, 200

    
if __name__ == '__main__':
    app.run()