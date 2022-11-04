import click
from flask import jsonify
from sqlalchemy import JSON

from main.app import app
from main.models import Advert, Category
from main.view import *

# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', filename='log.log')






@app.route('/item/<int:item_id>')
@app.route('/items')
def items(item_id=None):
    return Category.fs_get_delete_put_post(item_id)









if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)