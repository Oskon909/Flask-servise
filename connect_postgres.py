import psycopg2
from psycopg2 import Error


def get_table():
    connection = psycopg2.connect(user="postgres",
                                  # пароль, который указали при установке PostgreSQL
                                  password="akul6999",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="flask")
    cursor = connection.cursor()
    try:
        # Подключение к существующей базе данных
        connection = psycopg2.connect(user="postgres",
                                      # пароль, который указали при установке PostgreSQL
                                      password="akul6999",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="flask")

        # Курсор для выполнения операций с базой данных
        cursor = connection.cursor()
        postgreSQL_select_Query = "select * from Category"
        # ----------------------------------
        cursor.execute(postgreSQL_select_Query)
        print("Выбор строк из таблицы mobile с помощью cursor.fetchall")
        category = cursor.fetchall()
        # for i in mobile_records:
        #     print(i)
        # ----------------------------------
        postgreSQL_select_Query2 = "select * from SubCategory"

        cursor.execute(postgreSQL_select_Query2)
        print("Выбор строк из таблицы mobile с помощью cursor.fetchall")
        subcategory = cursor.fetchall()
        # --------------------------------

        postgreSQL_select_Query_city = "select * from City"
        cursor.execute(postgreSQL_select_Query_city)
        city = cursor.fetchall()

        postgreSQL_select_Query_advert = "select * from Advert"
        cursor.execute(postgreSQL_select_Query_advert)
        advert = cursor.fetchall()


        # ----------------------------------
        # Распечатать сведения о PostgreSQL
        print("Информация о сервере PostgreSQL")
        print(connection.get_dsn_parameters(), "\n")
        # Выполнение SQL-запроса
        cursor.execute("SELECT version();")
        # Получить результат
        record = cursor.fetchone()
        print("Вы подключены к - ", record, "\n")

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:

        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")

    return category  #, subcategory, city, advert

print(get_table())