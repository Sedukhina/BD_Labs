from flask import Flask, render_template, redirect, url_for, request
import sqlalchemy
import sqlalchemy.orm
import redis
import pymongo
from bson.decimal128 import Decimal128
import decimal
import time

from typing import Dict, Any
import hashlib
import json
from bson.objectid import ObjectId

r_postgres = redis.Redis(host='redis', port=6379, db=0)
r_mongo = redis.Redis(host='redis', port=6379, db=1)

username = 'username'
password = 'password'
database = 'database'
host = 'db'
port = '5432'

url = "postgresql://" + username + ":" + password + "@" + host + "/" + database

mongo_client = pymongo.MongoClient("mongodb://username:password@mongo:27017/")

mongo_db = mongo_client["database"]

#url_redis = "redis:///?Server=redis&Port=6379&Password=password"

engine = sqlalchemy.create_engine(url, echo=True)

class Base(sqlalchemy.orm.DeclarativeBase): pass

class Student(Base):
    __tablename__ = 'students'

    student_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True, autoincrement=True)
    outid = sqlalchemy.Column(sqlalchemy.String)
    birth = sqlalchemy.Column(sqlalchemy.Integer)
    year = sqlalchemy.Column(sqlalchemy.Integer)
    territory_id = sqlalchemy.Column(sqlalchemy.Integer)
    registration_type = sqlalchemy.Column(sqlalchemy.Integer)
    class_profile = sqlalchemy.Column(sqlalchemy.Integer)
    class_language = sqlalchemy.Column(sqlalchemy.Integer)
    sex_type = sqlalchemy.Column(sqlalchemy.Integer)
    eo_id = sqlalchemy.Column(sqlalchemy.Integer)

class Region(Base):
    __tablename__ = 'regions'

    region_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True, autoincrement=True)
    regname = sqlalchemy.Column(sqlalchemy.String)

class Area(Base):
    __tablename__ = 'areas'

    area_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True, autoincrement=True)
    areaname = sqlalchemy.Column(sqlalchemy.String)
    region_id = sqlalchemy.Column(sqlalchemy.Integer)
   

class Territory(Base):
    __tablename__ = 'territories'

    territory_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True,  autoincrement=True)
    territory_name = sqlalchemy.Column(sqlalchemy.String)
    territory_type = sqlalchemy.Column(sqlalchemy.Integer)
    area_id = sqlalchemy.Column(sqlalchemy.Integer)    

class RegistrationType(Base):
    __tablename__ = 'registration_types'

    type_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True,  autoincrement=True)
    type_name = sqlalchemy.Column(sqlalchemy.String)

class ClassProfile(Base):
    __tablename__ = 'class_profiles'
    
    profile_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True,  autoincrement=True)
    profile_name = sqlalchemy.Column(sqlalchemy.String)

class ClassLanguages(Base):
    __tablename__ = 'class_languages'
    
    lang_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True,  autoincrement=True)
    language = sqlalchemy.Column(sqlalchemy.String)    

class SexType(Base):
    __tablename__ = 'sex_types'

    type_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True,  autoincrement=True)
    sex_type = sqlalchemy.Column(sqlalchemy.String)

class  EO_Type(Base):
    __tablename__ = 'eo_types'
    
    type_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True,  autoincrement=True)
    type_name = sqlalchemy.Column(sqlalchemy.String)  

class  EO_Parent(Base):
    __tablename__ = 'eo_parents'
    
    parent_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True,  autoincrement=True)
    parent_name = sqlalchemy.Column(sqlalchemy.String)  

class EducationalOrganization(Base):
    __tablename__ = 'educational_organizations'

    eo_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True,  autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    territory_id = sqlalchemy.Column(sqlalchemy.Integer)
    type = sqlalchemy.Column(sqlalchemy.Integer)
    parent = sqlalchemy.Column(sqlalchemy.Integer)

class TestResult(Base):
    __tablename__ = 'test_results'

    test_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True,  autoincrement=True)
    student_id = sqlalchemy.Column(sqlalchemy.Integer)
    subject_id = sqlalchemy.Column(sqlalchemy.Integer)
    language_id = sqlalchemy.Column(sqlalchemy.Integer)
    dpa_level = sqlalchemy.Column(sqlalchemy.String)
    status_id = sqlalchemy.Column(sqlalchemy.Integer)
    ball100 = sqlalchemy.Column(sqlalchemy.Numeric(6,2))
    ball12 = sqlalchemy.Column(sqlalchemy.Numeric(6,2))
    ball = sqlalchemy.Column(sqlalchemy.Numeric(6,2))
    adaptscale = sqlalchemy.Column(sqlalchemy.Numeric(6,2))
    subtest = sqlalchemy.Column(sqlalchemy.Boolean)
    eo_id = sqlalchemy.Column(sqlalchemy.Integer)

class TestStatus(Base):
    __tablename__ = "test_statuses"
    
    status_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True,  autoincrement=True)
    status = sqlalchemy.Column(sqlalchemy.String)  

class Subject(Base):
    __tablename__ = 'subjects'

    subject_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True,  autoincrement=True)
    subject = sqlalchemy.Column(sqlalchemy.String)

app = Flask(__name__)

def MongoMigration():
    start_time = time.time()
    tables = GetTablesNames()
    for table in tables:
        with sqlalchemy.orm.Session(autoflush=False, bind=engine) as db:
                pass
        md = GetModel(table)
        col = mongo_db[table]
        lst = []
        i = 0
        for row in db.query(md).all():
            dictret = dict(row.__dict__)
            dictret.pop('_sa_instance_state', None)
            if(table == "TestResult"):
                for k, v in list(dictret.items()):
                    if isinstance(v, decimal.Decimal):
                        dictret[k] = Decimal128(str(v))
            lst.append(dictret)
            #col.insert_one(dictret)
            i += 1
            if(i%10000 == 0):
                col.insert_many(lst)
                lst = []
        col.insert_many(lst)  
    end_time = time.time()

    print("Mongo migration time: ", end_time-start_time)  

def GetTablesNames():
    TableNames = []
    for mapper in Base.registry.mappers:
        cls = mapper.class_
        #print(cls.__table__.columns)
        TableNames.append(cls.__name__)
    return TableNames

def GetModel(model):
    for mapper in Base.registry.mappers:
        cls = mapper.class_
        if(cls.__name__ == model):
            return mapper.class_

def GetColumns(model):
    mapper = sqlalchemy.inspect(model)
    columns = []
    for column in mapper.attrs:
        columns.append(column.key)
    return columns


#CRUD Functions
def Insert(Row, Mongo, model_name):
    if(Mongo):
        col = mongo_db[model_name]
        #col.insert_one(Row)
        return [["No insertoins in Mongo"]]
    else:
        with sqlalchemy.orm.Session(autoflush=False, bind=engine) as db:
            pass
        db.add(Row)
        db.commit()
    return [["Inserted"]]

def list_to_string(lst):
    strn = ""
    for l in lst:
        strn += str(l)
        strn += ";"
    return strn 

def dict_hash(dictionary: Dict[str, Any]) -> str:
    dhash = hashlib.md5()
    encoded = json.dumps(dictionary, sort_keys=True).encode()
    dhash.update(encoded)
    return dhash.hexdigest()

def Read(model, filters, mongo, model_name):
    hash_f = dict(filters)
    hash_f["model"] = model_name
    query_cache_key = dict_hash(hash_f)
    if(mongo):
        lst = r_mongo.lrange(query_cache_key, 0, -1)
        if(lst != []):
            print("CACHE")
            nlist = []
            for l in lst:
                l = bytes.decode(l, 'utf-8')
                l = l.split(";")
                nlist.append(l)
            return nlist

        if("_id") in filters:
           filters["_id"] = ObjectId(filters.get("_id"))
        for k, v in list(filters.items()):
            if(k != "_id"):
                if(v.isdigit()):
                    filters[k] = int(v)
        collection = mongo_db[model_name]
        details = collection.find(filters)
        lst_d = list(details)
        lst = []
        if(len(lst_d) != 0):
            lst.append(lst_d[0])
            r_mongo.lpush(query_cache_key, list_to_string(lst_d[0]))

        for doc in lst_d:
            ld = doc.values()
            lst.append(ld)
            r_mongo.lpush(query_cache_key, list_to_string(ld))
        
        r_mongo.expire(query_cache_key, 60)
        
        return lst
    else:    
        lst = r_postgres.lrange(query_cache_key, 0, -1)
        if(lst != []):
            print("CACHE")
            nlist = []
            for l in lst:
                l = bytes.decode(l, 'utf-8')
                l = l.split(";")
                nlist.append(l)
            return nlist

        with sqlalchemy.orm.Session(autoflush=False, bind=engine) as db:
            pass
        query = db.query(model).filter_by(**filters)
        result = query.all()
        columns = GetColumns(model)
        res_list = []

        for row in result:
            row_list = []
            for column in columns:
                row_list.append(getattr(row, column))
            r_postgres.lpush(query_cache_key, list_to_string(row_list))
            res_list.append(row_list)
        r_postgres.expire(query_cache_key, 60)
        return res_list
            

def Delete(model, filters, mongo,  model_name):
    if(not mongo):
        with sqlalchemy.orm.Session(autoflush=False, bind=engine) as db:
            pass
        db.query(model).filter_by(**filters).delete()
        db.commit()
        return [["Deleted succesfully"]]
    else:
        if("_id") in filters:
           filters["_id"] = ObjectId(filters.get("_id"))
        for k, v in list(filters.items()):
            if(k != "_id"):
                if(v.isdigit()):
                    filters[k] = int(v)
        collection = mongo_db[model_name]
        collection.delete_many(filters)
        return [["Deleted succesfully"]]

@app.route('/')
@app.route('/index')
def home():
    return render_template("index.html", tables = GetTablesNames())

@app.route('/query', methods=["POST"])
def query():
    model_name = request.form.get('model')

    model = GetModel(model_name)  
    columns = GetColumns(model)

    return render_template("query.html", tables = GetTablesNames(), model = model_name, columns=columns)

@app.route('/query_result', methods=["POST"])
def query_result():
    with sqlalchemy.orm.Session(autoflush=False, bind=engine) as db:
        pass

    Mongo = False
    if(request.form.get('mongo')):
        Mongo = True

    model_name = request.form.get('model')
    model = GetModel(model_name)  
    columns = GetColumns(model)

    try:
        action = request.form.get('action')

        query_res = [[]]

        if(action == "Insert"):
            if(Mongo):
                Row = {}
                first_col = True
                for column in columns:
                    if(first_col == False):
                        col = request.form.get(column)
                        if(col != ""):
                            Row[column] = request.form.get(column)
                    else:
                        first_col = False
                    query_res = Insert(Row, Mongo, model_name)
            else:
                Row = model()
                first_col = True
                for column in columns:
                    if(first_col == False):
                        col = request.form.get(column)
                        if(col != ""):
                            setattr(Row, str(column), request.form.get(column))
                    else:
                        first_col = False
                    query_res = Insert(Row, Mongo)

        if(action == "Read" or action == "Delete"):
            filters = {}
            first_col_m = False
            if(Mongo):
                first_col_m = True
            for column in columns:
                if(first_col_m == False):
                    col = request.form.get(column)
                    if(col != ""):
                        filters[column] = col     
                else:
                    col = request.form.get(column)
                    print(column)
                    if(col != ""):
                        filters["_id"] = col
                    first_col_m = False
            if(action == "Read"):          
                query_res = Read(model, filters, Mongo, model_name)
            else:
                query_res = Delete(model, filters, Mongo, model_name)
    
        return render_template("query_result.html", tables = GetTablesNames(), model = model_name, columns=columns, query_res=query_res)        
    except:
        return render_template("query_result.html", tables = GetTablesNames(), model = model_name, columns=columns, query_res=[["Invalid Query"]])
    

@app.route('/main_query', methods=["POST"])
def main_query():
    with sqlalchemy.orm.Session(autoflush=False, bind=engine) as db:
        pass
    return render_template("main_query.html", years = db.query(sqlalchemy.distinct(Student.year)), regions = db.query(Region.regname).distinct().all(), subjects = db.query(Subject.subject).distinct().all(), tables = GetTablesNames())

@app.route('/main_query_result', methods=["POST"])
def main_query_res():
    with sqlalchemy.orm.Session(autoflush=False, bind=engine) as db:
        pass
    checked_years = request.form.getlist("years")
    for i in range(len(checked_years)):
        checked_years[i] = checked_years[i].replace("(", "").replace("'", "").replace(")", "").replace(",", "")

    checked_subjects = request.form.getlist("subjects")
    for i in range(len(checked_subjects)):
        checked_subjects[i] = checked_subjects[i].replace("(", "").replace("'", "").replace(")", "").replace(",", "")
 
    #db.query(Subject.subject_id.filter_by)
    checked_regions = request.form.getlist("regions")
    for i in range(len(checked_regions)):
        checked_regions[i] = checked_regions[i].replace("(", "").replace("'", "").replace(")", "").replace(",", "")

    balls = db.query(sqlalchemy.func.max(TestResult.ball), Student.year, Region.regname, Subject.subject).join(Subject, Subject.subject_id == TestResult.subject_id).join(Student, Student.student_id == TestResult.student_id).join(EducationalOrganization, EducationalOrganization.eo_id == TestResult.eo_id).join(Territory, Territory.territory_id == EducationalOrganization.territory_id).join(Area, Area.area_id == Territory.area_id).join(Region, Region.region_id == Area.region_id).filter(Subject.subject.in_(checked_subjects)).filter(Student.year.in_(checked_years)).filter(Region.regname.in_(checked_regions)).group_by(Student.year, Region.regname, Subject.subject)
    balls = balls.all()
    print(balls)
    return render_template("main_query_result.html", years = db.query(sqlalchemy.distinct(Student.year)), regions = db.query(Region.regname).distinct().all(), subjects = db.query(Subject.subject).distinct().all(), query_res = balls,  tables = GetTablesNames())

if __name__ == '__main__':
    r_postgres.ping()
    #MongoMigration()
    app.run(host="app", port=5555)