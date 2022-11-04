from flask import jsonify, request

from main.app import app
from main.models import Category, Advert
import json

@app.route('/get_data')
def post():
    data = json.loads(request.data)

    print(data['name'])
    print(data['description'])
    print(data['from_price'])
    # Advert(name=data['name'], description=data['description'], from_price=data['from_price'],).save()
    return jsonify({'status': 'ok'})





