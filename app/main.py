import psycopg2
import pandas
import time
import csv
import os 

username = 'username'
password = 'password'
database = 'database'
host = 'db'
port = '5432'

def connect(username, password, database, host, port):
    conn = None
    try:
        conn = psycopg2.connect(user=username, password=password, dbname=database, host=host, port=port)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return connect(username, password, database, host, port)
    return conn

def InsertOdataRows(conn, rows):
    try:
        rows_str = []
        for row in rows:
            rows_str.append(str(row).replace("nan", "null"))
        cur = conn.cursor()
        for row in rows_str:
            cur.execute("INSERT INTO Odata VALUES " + row)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.rollback()
        cur.close()
        return False
    return True

def TryExecute(conn, query, write = 0):
    try:
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
        if(write):
            file = open('query_result.csv', 'w', newline='')
            writer = csv.writer(file)
            result = cur.fetchall()
            for row in result:
                writer.writerow(row)
            print(os.path.abspath('query_result.csv'))
            file.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.rollback()
        cur.close()
        return False
    return True


Odata2019 = pandas.read_csv('Odata2019File.csv', sep=';', encoding="cp1251", na_values='null', keep_default_na=False, decimal=',')
Odata2020 = pandas.read_csv('Odata2020File.csv', sep=';', encoding="cp1251", na_values='null', keep_default_na=False, decimal=',')
Odata2021 = pandas.read_csv('Odata2021File.csv', sep=';', encoding="utf8", na_values='null', keep_default_na=False, decimal=',')

Odata2019['Year'] = 2019
Odata2020['Year'] = 2020
Odata2021['Year'] = 2021

Odata = pandas.concat([Odata2019, Odata2020], axis=0)

for i in Odata2021.columns:
    for n in Odata.columns:
        if i.lower() == n.lower():
            Odata2021.rename(columns={i: n}, inplace=True)

Odata = pandas.concat([Odata, Odata2021], axis=0)

CreateTable = 'CREATE TABLE IF NOT EXISTS Odata('
sql_columns = Odata.dtypes.to_string()
sql_columns = sql_columns.replace("object", "VARCHAR NULL,")
sql_columns = sql_columns.replace("int64", "NUMERIC(4) NULL,")
sql_columns = sql_columns.replace("float64", "NUMERIC(6,2) NULL,")
sql_columns = sql_columns.replace("OUTID VARCHAR NULL", "OUTID VARCHAR NULL")
sql_columns = sql_columns[:-1]
sql_columns = sql_columns + " );"
CreateTable = CreateTable+sql_columns

for i in Odata.columns:
     if(Odata[i].dtype == "object"):
         Odata[i] = Odata[i].str.replace("'", "`")

Odata = Odata.reset_index(drop=True)

conn = connect(username, password, database, host, port)
cur = conn.cursor()

start_time = time.time()

while(not TryExecute(conn, CreateTable)):
    conn = connect(username, password, database, host, port)
while(not TryExecute(conn, "Truncate Odata")):
    conn = connect(username, password, database, host, port)

tuples = [tuple(x) for x in Odata.to_numpy()]
sub_tup = []
for i in range(len(tuples)):
    sub_tup.append(tuples[i])
    if i%100000 == 0:
        while (not InsertOdataRows(conn, sub_tup)):
            conn = connect(username, password, database, host, port)
        sub_tup = []
#Last rows insertion 
while (not InsertOdataRows(conn, sub_tup)):
            conn = connect(username, password, database, host, port)


end_time = time.time()

print("Insertion time: ", end_time-start_time)

MainQuery = "select MAX(physball100), REGNAME, YEAR FROM ODATA GROUP BY REGNAME,YEAR, physteststatus HAVING physteststatus = 'Зараховано' AND(YEAR = 2019 OR YEAR = 2021)"
while(not TryExecute(conn, MainQuery, 1)):
    conn = connect(username, password, database, host, port)

