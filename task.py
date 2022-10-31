from app import app, Category
from celery_config import make_celery
from parsing import run_pars_selexy

celery = make_celery(app)



# Периодичный парсинг
@celery.task(name="periodic_task2")
def periodic_task2():
    run_pars_selexy()
    print('Hi! from periodic_task2')


@celery.task(name="periodic_task")
def periodic_task():
    print('Hi! from periodic_task')

#send data to django Advert model
@celery.task(name="send_data_to_django")
def send_data_to_django(data):
    Category.query.all()
    print(data)

    print('Hi! from send_data_to_django')





