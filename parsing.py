import asyncio
import os
import datetime
import boto3
import urllib.request
import requests
import aiohttp
from bs4 import BeautifulSoup

from app import Advert, Category, SubCategory, db, app, City

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.160 YaBrowser/22.5.3.673 Yowser/2.5 Safari/537.36"
}


# link_selexy = f'https://salexy.kg'
# post = requests.get(link_selexy, headers=headers)
# postsrc = post.text
#
#
# POSTSOUD = BeautifulSoup(postsrc, "lxml")
# deteil_post_links = []

def get_category(POSTSOUD):
    perl = POSTSOUD.find(class_='nav-list').find_all('a')
    list_category_link = []
    list_cateory_name = []

    for i in perl:
        if len(i['href'].split('/')) == 4:
            list_category_link.append(i['href'])
            list_cateory_name.append(i.text)

    return list_category_link, list_cateory_name


def get_subcategory(POSTSOUD):
    perl = POSTSOUD.find(class_='breadcrumb').find_all('span')
    return perl[-1].text


def get_img(POSTSOUD):
    posts = POSTSOUD.find(class_='main-content full-on-1024').find_all('img')
    print()
    if posts:
        img_link = posts[0]['src']
        if os.path.exists('media/images')!=True:
            os.mkdir('media/images')

        img = img_link.split('/')
        if img[-1].split('.')[-1] != 'jpg':
            return None
        urllib.request.urlretrieve(img_link, f'media/images/{img[-1]}')
        print(img[-1])
        return img[-1]


def get_title(POSTSOUD):
    title = POSTSOUD.find(class_='product-name')
    if title:
        return title.text


def get_town(POSTSOUD):
    town = POSTSOUD.find(class_='address')
    if town:
        return town.text


def get_price(POSTSOUD):
    price = POSTSOUD.find(class_='control-holder')
    if price:
        if price.text.split()[1].isdigit() == False:
            return 0

        return price.text.split()[1]


def get_email(POSTSOUD):
    email = POSTSOUD.find(class_='desc')
    if len(email.text.split()) >= 4 and email.text.split()[2] == 'Email:':
        return email.text.split()[-1]


def get_descrition(POSTSOUD):
    desc = POSTSOUD.find_all(class_='description')
    if desc:
        return desc[0].text.rstrip()



async def run_pars_selexy():
    count_post = 0
    link_selexy = f'https://salexy.kg'
    async with aiohttp.ClientSession() as session:
        async with session.get(link_selexy, headers=headers) as post:
            postsrc = await post.text()

            POSTSOUD = BeautifulSoup(postsrc, "lxml")
            list_link_category, list_name_category = get_category(POSTSOUD)

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

                        subcategory = get_subcategory(POSTSOUD)
                        title = get_title(POSTSOUD)
                        print(title)

                        price = get_price(POSTSOUD)
                        town = get_town(POSTSOUD)
                        description = get_descrition(POSTSOUD)

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
                                    print(cat.id)  # Не удалять пока

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
                                    print(subcategory.id)  # не удалять
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

                                # Upload a new file
                                count_post += 1
                                # img = get_img(POSTSOUD)
                                # if  os.path.exists(f'media/images/{img}') == True:
                                #
                                #     aser=str(alisa.id)
                                #
                                #     data = open(f'media/images/{img}', 'rb')
                                #     s3.Bucket('myservise').put_object(Key=aser, Body=data)





                        except Exception as x:
                            print(x)

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
    print(current_datetime_start)

    asyncio.run(run_pars_selexy())
    current_datetime = datetime.datetime.now()
    print(current_datetime-current_datetime_start)
