from bson.errors import InvalidId
from bson import ObjectId
from flask import Flask, jsonify, request
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

app = Flask(__name__)


def connect_db():
    client = MongoClient('mymongo_1', 27017)
    db = client['sl_bd']
    return db['good']


def work_with_db(method, obj):
    try:
        return method(obj)
    except ServerSelectionTimeoutError:
        return


@app.route('/<id_good>', methods=['GET'])
def get_good(id_good):
    goods_base = connect_db()
    try:
        good = work_with_db(goods_base.find_one, {'_id': ObjectId(id_good)})
        if good:
            return jsonify({'name': good['name']}), 200
        return jsonify({'error': 'no database connection'}), 503
    except InvalidId:
        return jsonify({'error': 'good not found'}), 200


@app.route('/', methods=['POST'])
def create_good():
    goods_base = connect_db()

    if not request.json.get('name_good'):
        return jsonify({'error': 'Invalid format data'}), 400

    good = {'name': request.json.get('name_good')}
    result = work_with_db(goods_base.insert_one, good)

    if result:
        return jsonify({'_id': str(result.inserted_id), 'name': good['name']}), 200
    return jsonify({'error': 'no database connection'}), 503


if __name__ == '__main__':
    app.run(debug=False)
