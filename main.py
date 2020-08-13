from bson.errors import InvalidId
from bson import ObjectId
from flask import Flask, jsonify, request
from pymongo import MongoClient


app = Flask(__name__)

def connect_db():
    client = MongoClient('mymongo_1', 27017)
    db = client['test_bd']
    return db['good']


@app.route('/<id_good>', methods=['GET'])
def get_good(id_good):
    goods_base = connect_db()
    try:
        good = goods_base.find_one({'_id': ObjectId(id_good)})
        return jsonify({'name': good['name']}), 200
    except InvalidId:
        return jsonify({'error': 'good not found'}), 200


@app.route('/', methods=['POST'])
def create_good():
    goods_base = connect_db()

    if not request.json.get('name_good'):
        return jsonify({'error': 'Invalid format data'}), 400

    good = {'name': request.json.get('name_good')}
    result = goods_base.insert_one(good)
    return jsonify({'_id': str(result.inserted_id), 'name': good['name']})


if __name__ == '__main__':
    app.run(debug=False)
