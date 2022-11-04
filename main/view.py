from flask import jsonify, request

from main.app import app
from configuration.config import db
from main.models import Advert
import json

@app.route('/get_data')
def post():
    data = json.loads(request.data)
    advert = Advert(name=data['name'], description=data['description'],
                    from_price=data['from_price'],owner=data['owner']
                    ,email=data['email'],wa_number=data['wa_number'],
                    status=data['status'],category=data['category'])
    db.session.add(advert)
    db.session.commit()
    return jsonify({'status': 'ok'})


@app.route('/get')
def poster():
    data = json.loads(request.data)
    print(data)

    return jsonify({'status': 'ok'})





