from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import os


hive = create_engine('hive://54.180.199.24:10000/life_portfolio')

user = os.environ['MARIA_USER']
password = os.environ['MARIA_PASS']
maria = create_engine(f'mariadb://{user}:{password}@43.202.3.249:3306/upbit_dl_db')

hive_session = Session(hive)
maria_session = Session(maria)

