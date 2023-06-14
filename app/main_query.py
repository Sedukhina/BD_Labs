import psycopg2
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

MainQuery = '''select regname, max(ball) from test_results 
join subjects on test_results.subject_id = subjects.subject_id 
join educational_organizations on test_results.eo_id = educational_organizations.eo_id 
join Territories on educational_organizations.Territory_ID = Territories.Territory_ID 
join Areas on Territories.Area_ID = Areas.Area_ID
join Regions on Areas.Region_ID = Regions.Region_ID
group by regname, subject having subject = 'Фізика';'''

conn = connect(username, password, database, host, port)
while(not TryExecute(conn, MainQuery, 1)):
    conn = connect(username, password, database, host, port)
