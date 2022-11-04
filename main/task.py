import requests

from main.app import app
from main.celery_config import make_celery
from main.models import Category
from main.parsing import run_pars_selexy

celery = make_celery(app)



# Периодичный парсинг
@celery.task(name="periodic_task2")
def periodic_task2():
    run_pars_selexy()
    print('Hi! from periodic_task2')


@celery.task(name="periodic_task")
def periodic_task():
    print('Hi! from periodic_task')


@celery.task(name="send_data_to_django")
def send_data_to_django():

    data=Category.fs_get_delete_put_post()
    response = requests.post('http://127.0.0.1:8000/get_data', json={'data': data})
    print(response.json())
    print('Hi! from send_data_to_django')





