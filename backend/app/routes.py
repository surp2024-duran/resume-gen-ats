# backend/app/routes.py
from flask import Blueprint, jsonify, request
from app.models import db
import logging
from bson import ObjectId
import json

main_routes = Blueprint('main', __name__)

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime.datetime):
            return o.isoformat()
        return super(JSONEncoder, self).default(o)

@main_routes.route('/data', methods=['GET'])
def get_collections():
    try:
        collections = db.list_collection_names()
        logging.info(f"Collections found: {collections}")
        if not collections:
            return jsonify({"message": "No collections found in the database."}), 404
        else:
            return jsonify({"collections": collections}), 200
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500

@main_routes.route('/data/<collection_name>', methods=['GET'])
def get_collection_data(collection_name):
    try:
        collection = db[collection_name]
        documents = list(collection.find())
        for doc in documents:
            if 'created_at' in doc:
                doc['created_at'] = doc['created_at'].isoformat()
        logging.info(f"Documents found in {collection_name}: {documents}")
        return JSONEncoder().encode(documents), 200
    except Exception as e:
        logging.error(f"An error occurred while fetching data from {collection_name}: {str(e)}")
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500
