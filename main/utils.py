import hashlib
import requests

from collections import OrderedDict
from bs4 import BeautifulSoup
from flask import jsonify
from main.app import app





def generate_sig(data: dict, method: str):
    data = OrderedDict(sorted(data.items()))
    string = method

    for key, value in data.items():
        if value and key != 'pg_sig':
            string += ";{}".format(value)

    string += ";{}".format("LeFnP16MP6AU6YKc")
    pg_sig = hashlib.md5(string.encode()).hexdigest()
    data['pg_sig'] = pg_sig
    return data



def get_url_from_content_result(html: str, teg: str):
    soup = BeautifulSoup(html, 'html.parser')
    return soup.find(teg).text


def get_url_from_content(html: str):
    soup = BeautifulSoup(html, 'html.parser')
    return soup.find('pg_redirect_url').text




@app.route('/pay/<int:pk>/<int:pt>', methods=['GET'])
def get(pk, pt):

    # post = Advert.query.get(pk=pk)
    method = 'init_payment.php'
    print(pk,pt)
    # sub = Subscription.objects.filter(pk=pn).values('price')
    # price = int(sub[0]['price'])
    price='20'
    data = dict(
        pg_order_id=id,
        pg_merchant_id=535456,
        pg_amount=price,
        pg_description='some',
        pg_success_url='http://127.0.0.1:5000/api/success',
        pg_failure_url='http://127.0.0.1:5000/api/failure',
        pg_salt='some',
    )

    payment = generate_sig(data, method)
    params = payment
    base_url = 'https://api.paybox.money/'
    r = requests.post(f"{base_url}{method}", params=params)
    url = get_url_from_content(r.content)
    payment_id = 'pg_payment_id'
    payment = get_url_from_content_result(r.content, payment_id)

    # data = redis.Redis()
    # data.mset({'pk': pk})
    # data.mset({'pn': pn})
    return jsonify({'redirect': url})
