import urllib.parse, urllib.error, urllib.request
from bs4 import BeautifulSoup
import sqlite3



def stockcheck():
    fh = urllib.request.urlopen('https://finance.yahoo.com/most-active')
    ans = fh.read()
    soup = BeautifulSoup(ans,'html.parser')


    lst = list(soup.strings)

#stores stock prices in stocklst
    stocklst = []
    face = False#Used to omit text that isn't stock prices
    for i in lst:
        if i == '52 Week Range':
            face = True
            continue
        if face == True:
            stocklst.append(i)
        if i[0:2] == 'if' :
            face = False

    stocklst.pop()# Removes unecessary 'if line'


    #stores stock prices in a list of tuples
    tuple_lst = []

    while len(stocklst) > 0:
        tuple_lst.append((stocklst[0],stocklst[1],stocklst[2],stocklst[3],stocklst[4],stocklst[5],stocklst[6],stocklst[7],stocklst[8]))
        del(stocklst[:9])

    for i in tuple_lst:
        print(i)

# put the info from tuple_lst into a database via sqlite
    conn = sqlite3.connect('yahoostock.db')
    cur = conn.cursor()

    cur.executescript('''
        DROP TABLE IF EXISTS Stocks;

        CREATE TABLE Stocks(
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        price TEXT ,
        change TEXT ,
        percent_change TEXT ,
        volume TEXT ,
        avg_vol_3_month TEXT ,
        market_cap TEXT ,
        pe_ratio TEXT
        );

        ''')

    for item in tuple_lst:
        cur.execute('''INSERT INTO Stocks
        (name, price, change, percent_change, volume, avg_vol_3_month, market_cap, pe_ratio)
        VALUES(?,?,?,?,?,?,?,?)''',
        (item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7]))

    conn.commit()

stockcheck()
