import requests
import datetime
from datetime import timedelta
import mysql.connector
from mysql.connector import errorcode
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import collections
import re

from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#simple create db if not exist
def create_db():
    db_config={'host': 'localhost',  'port': 5883, 
                'user': 'root', 'password':'root', 'database': 'currency' }
    try: 
        db = mysql.connector.connect(
        host = db_config['host'],
        port = db_config['port'],
        user = db_config['user'],
        password = db_config['password'],
        database = db_config['database']
            )
    except mysql.connector.Error as err:
        db = mysql.connector.connect(
        host = db_config['host'],
        port = db_config['port'],
        user = db_config['user'],
        password = db_config['password'],
               )
        mycursor = db.cursor()
        mycursor.execute("CREATE DATABASE currency")


# for the first goal of the task
def main():
    r = requests.get('https://api.exchangeratesapi.io/latest?base=USD')
    create_db()
    engine = create_engine("mysql+pymysql://root:root@localhost:5883/currency?charset=utf8mb4")
    Base = declarative_base()
    Session = sessionmaker(bind = engine)
    session = Session()

    class Currency(Base):
        __tablename__='currency'
        id = Column(Integer, primary_key=True)
        currency_name = Column(String(50))
        rate =Column(Float)
        date_request = Column(DateTime)

        def __init__(self, currency_name, rate, date_request):
            self.currency_name=currency_name
            self.rate = rate
            self.date_request = date_request
    
    Base.metadata.create_all(engine)

    time_delta = timedelta(minutes=10)

    if r.status_code == 200:
        date_request = datetime.datetime.now()
        output_dict = {}
        for key, value in r.json()['rates'].items():
            ext_currency = session.query(Currency).filter(Currency.currency_name==key).first()
            if ext_currency:
                #checker whether datetime.now() is grater than previous request time
                if datetime.datetime.now() > ext_currency.date_request + time_delta:
                        ext_currency.rate = round(value, 3)
                        ext_currency.date_request = datetime.datetime.now()  
                        output_dict[key]=round(value, 3)
                        session.commit()
                else:
                    print('this is ext_curr ' + str(ext_currency.currency_name))
                    output_dict[ext_currency.currency_name]=ext_currency.rate
            else:
                print('nothing to db')
                output_dict[key]=round(value, 3)
                currency = Currency(key, round(value, 3), date_request)
                session.add(currency)
                session.commit()
    return output_dict


#for re(exchnage operation)
def find_str(text):
    my_dict = main()
    match = re.findall("[$]", text)
    if match:
        new_str = re.sub("[$%]","", text)
        new_list = new_str.split(" ")
        curr_amount=float(new_list[1])
        print(new_list)
    else:
        new_list = text.split(" ")
        curr_amount=float(new_list[1])
    exch_currency = new_list[-1]
    total_exch_rate = round(curr_amount * my_dict[exch_currency], 2)
    print('this is curr_amount: ' + str(curr_amount))
    print('this is my_dict[exch_currency]: ' + str(my_dict[exch_currency]))
    return '$' + str(total_exch_rate)

def history_task(my_command):
    
    end_date = datetime.date.today()
    my_list = my_command.split(' ')
    #pick up period from list and makes it timedelta
    new_period = my_list[-2]
    new_period_time = timedelta(days=int(new_period))
    #makes new str from split and grab the currencies
    new_str=','.join(my_list[1])
    curr_list_chcarter=new_str.split(',')
    currency_base = (curr_list_chcarter[0]+curr_list_chcarter[1]+curr_list_chcarter[2])
    currency_symbols = ((curr_list_chcarter[-3]+curr_list_chcarter[-2]+curr_list_chcarter[-1]))


    r = requests.get('https://api.exchangeratesapi.io/history?start_at={}&end_at={}&base={}&symbols={}'.format(
                                                    end_date - new_period_time ,
                                                    end_date,
                                                    currency_base,
                                                   currency_symbols))

    my_dict = r.json()['rates']
    #check if web service return any data
    if len(my_dict) > 1:
        print(len(my_dict))
        #sort dict by date before make a df and plot
        od = collections.OrderedDict(sorted(my_dict.items()))
        df = pd.DataFrame(od)
        #from horizont to vertical df
        df1=df.T
        df1.plot()
        fig = plt.gcf()
        fig.savefig('./output.png')
        path = './output.png'
        return str(path)
    else:
        mess = 'No exchange rate data is available for the selected currency.'
        return mess
    


if __name__ == "__main__":
    (main())
    

    
    




















