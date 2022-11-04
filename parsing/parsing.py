import asyncio
import os
import datetime
import boto3
import urllib.request
import requests
import aiohttp
from bs4 import BeautifulSoup
from main.models import Advert, Category, SubCategory, City

from main.app import app
from configuration.config import db
import logging

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.160 YaBrowser/22.5.3.673 Yowser/2.5 Safari/537.36"
}


def get_category(POSTSOUD):
    perl = POSTSOUD.find(class_='nav-list').find_all('a')
    list_category_link = []
    list_cateory_name = []

    for i in perl:
        if len(i['href'].split('/')) == 4:
            list_category_link.append(i['href'])
            list_cateory_name.append(i.text)
    return list_category_link, list_cateory_name


def get_img(POSTSOUD):
    posts = POSTSOUD.find(class_='main-content full-on-1024').find_all('img')
    print()
    if posts:
        img_link = posts[0]['src']
        if os.path.exists('../media/images') != True:
            os.mkdir('../media/images')
        img = img_link.split('/')

        if img[-1].split('.')[-1] != 'jpg':
            return None
        urllib.request.urlretrieve(img_link, f'../media/images/{img[-1]}')
        return img[-1]


async def run_pars_selexy():
    count_post = 0
    link_selexy = f'https://salexy.kg'
    async with aiohttp.ClientSession() as session:
        post = requests.get(link_selexy, headers=headers)
        POSTSOUD = BeautifulSoup(post.text, "lxml")
        list_link_category, list_name_category = get_category(POSTSOUD)
        print('------------------')
        for link, name_category in enumerate(list_name_category):
            for q in range(1, 2):
                async with session.get(f'{list_link_category[link]}?page={q}', headers=headers) as post:
                    postsrc = await post.text()

                with open(f'{q}.html', 'w') as file:
                    file.write(postsrc)
                with open(f'{q}.html') as file:
                    postsrc = file.read()

                POSTSOUD = BeautifulSoup(postsrc, "lxml")
                deteil_post_links = []
                posts = POSTSOUD.find(class_="product-list").find_all("a")
                for k in posts:
                    Iten_href1 = k.get("href")
                    deteil_post_links.append(Iten_href1)

                anti_copy = []
                for i in deteil_post_links:
                    if i in anti_copy:
                        continue

                    anti_copy.append(i)
                    async with session.get(i, headers=headers) as post:
                        postsrc = await post.text()

                    POSTSOUD = BeautifulSoup(postsrc, "lxml")
                    subcategory_html = POSTSOUD.find(class_='breadcrumb').find_all('span')
                    subcategory = subcategory_html[-1].text

                    if POSTSOUD.find(class_='product-name'):
                        title = POSTSOUD.find(class_='product-name').text
                    else:
                        title = 'Не указано'

                    price = POSTSOUD.find(class_='control-holder')
                    if price:
                        if price.text.split()[1].isdigit() == False:
                            price = 0
                        else:
                            price = price.text.split()[1]

                    if POSTSOUD.find(class_='address'):
                        town = POSTSOUD.find(class_='address').text
                    else:
                        town = 'Не указано'

                    desc = POSTSOUD.find_all(class_='description')
                    if desc:
                        description = desc[0].text.rstrip()
                    else:
                        description = 'Не указано'

                    with app.app_context():
                        rest = Category.query.all()
                        for i in rest:
                            if i.name == name_category.split()[1:][0]:
                                cat = i
                                break
                        else:
                            with app.app_context():
                                cat = Category(name=name_category.split()[1:][0])
                                db.session.add(cat)
                                db.session.commit()

                    try:
                        with app.app_context():
                            sub = SubCategory.query.all()
                            for h in sub:
                                if h.name == subcategory:
                                    subcategory = h
                                    break
                            else:
                                subcategory = SubCategory(category=cat.id, name=subcategory)
                                db.session.add(subcategory)
                                db.session.commit()
                    except:
                        with app.app_context():
                            subcategory = SubCategory(category=cat.id, name=subcategory)
                            db.session.add(subcategory)
                            db.session.commit()
                    try:
                        with app.app_context():
                            db.create_all()
                            city = City(name=town)
                            db.session.add(city)
                            db.session.commit()
                            alisa = Advert(owner=1, category=cat.id,
                                           subcategory=subcategory.id,
                                           name=title, city=city.id,
                                           from_price=price,
                                           description=description)

                            db.session.add(alisa)
                            db.session.commit()
                            s3 = boto3.resource('s3', aws_access_key_id='AKIA4LJFIHLRIJSNYFNS',
                                                aws_secret_access_key='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')

                            count_post += 1
                            img = get_img(POSTSOUD)
                            if os.path.exists(f'../media/images/{img}') == True:
                                key_picter = str(alisa.id)
                                data = open(f'../media/images/{img}', 'rb')
                                s3.Bucket('myservise').put_object(Key=key_picter, Body=data)

                    except Exception as x:
                        logging.error(x)
                    print(count_post)
                    if count_post == 15:
                        break
                os.remove(f'{q}.html')
                if count_post == 15:
                    break
            if count_post == 15:
                break


if __name__ == '__main__':
    current_datetime_start = datetime.datetime.now()
    asyncio.run(run_pars_selexy())
    current_datetime = datetime.datetime.now()
    print(current_datetime - current_datetime_start)
