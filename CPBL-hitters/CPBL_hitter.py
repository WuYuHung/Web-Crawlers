import sqlite3
import json
import pandas as pd
from lxml import html
from bs4 import BeautifulSoup

START_YEAR = 2010
END_YEAR = 2016
BASIC_URL = "http://www.cpbl.com.tw/games/box.html?&game_type=01&pbyear="

conn = sqlite3.connect('CPBL_hitters')

cur = conn.cursor()

with open('cpbl.json') as data_file:
    data = json.load(data_file)

for y in range(START_YEAR, END_YEAR + 1):
    year = str(y)
    id_list = data['01'][year]
    for i, j in id_list.items():
        for n in j:
            url = BASIC_URL + "{year}&game_id={id}&game_date={year}-{month}-{day}".format(
                year=year, id=n, month=i[:2], day=i[-2:])
            try:
                df = pd.read_html(url)
                for N in [7, 8]:
                    for v in range(1, df[N].shape[0] - 1):
                        places = df[N][0][v].split(',')
                        place = places[1].replace(' ', '')
                        if place[0] == '(':
                            place = place[1:]
                        place = place.replace('(', ', ')
                        place = place.replace(')', '')
                        datas = [df[N][j][v] for j in range(1, 18)]
                        table_name = places[0].replace(' ', '')
                        team = df[N][0][0]
                        date = '{year}/{month}/{day}'.format(
                            year=year, month=i[:2], day=i[-2:])
                        cur.execute(("create table if not exists '{name}' ('TEAM', 'DATE','PLACE', 'AB', 'R', 'H',"
                                     "'RBI','2B','3B', 'HR', 'GIDP', 'BB','HBP', 'SO','SAC','SF', 'SB','CS', 'E', 'AVG')").format(name=table_name))
                        exestr = ("insert into '{name}' ('TEAM', 'DATE','PLACE', 'AB', 'R', 'H',"
                                  "'RBI','2B','3B', 'HR', 'GIDP', 'BB','HBP', 'SO','SAC','SF', 'SB','CS', 'E', 'AVG')values ('{team}', '{date}','{place}'").format(name=table_name, team=team, date=date, place=place)
                        for k in datas:
                            exestr += (",\'" + str(k) + "\'")
                        exestr += ")"
                        cur.execute(exestr)
            except:
                pass
conn.close()
