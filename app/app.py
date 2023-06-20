from flask import Flask, render_template, redirect, url_for, request
import sqlalchemy
import sqlalchemy.orm
import redis

r = redis.Redis(host='redis', port=6379, db=0)

username = 'username'
password = 'password'
database = 'database'
host = 'db'
port = '5432'

url = "postgresql://" + username + ":" + password + "@" + host + "/" + database
engine = sqlalchemy.create_engine(url, echo=True)

class Base(sqlalchemy.orm.DeclarativeBase): pass

class Student(Base):
    __tablename__ = 'students'

    student_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True)
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

    region_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True)
    regname = sqlalchemy.Column(sqlalchemy.String)

class Subject(Base):
    __tablename__ = 'subjects'

    subject_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True)
    subject = sqlalchemy.Column(sqlalchemy.String)

class TestResult(Base):
    __tablename__ = 'test_results'

    test_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True)
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

class EducationalOrganization(Base):
    __tablename__ = 'educational_organizations'
    eo_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    territory_id = sqlalchemy.Column(sqlalchemy.Integer)
    type = sqlalchemy.Column(sqlalchemy.Integer)
    parent = sqlalchemy.Column(sqlalchemy.Integer)

class Territory(Base):
    __tablename__ = 'territories'

    territory_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True)
    territory_name = sqlalchemy.Column(sqlalchemy.String)
    territory_type = sqlalchemy.Column(sqlalchemy.Integer)
    area_id = sqlalchemy.Column(sqlalchemy.Integer)

class Area(Base):
    __tablename__ = 'areas'

    area_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True)
    areaname = sqlalchemy.Column(sqlalchemy.String)
    region_id = sqlalchemy.Column(sqlalchemy.Integer)

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def home():
    with sqlalchemy.orm.Session(autoflush=False, bind=engine) as db:
        pass
    return render_template("index.html", years = db.query(sqlalchemy.distinct(Student.year)), regions = db.query(Region.regname).distinct().all(), subjects = db.query(Subject.subject).distinct().all())

@app.route('/query', methods=["POST"])
def query_res():
    with sqlalchemy.orm.Session(autoflush=False, bind=engine) as db:
        pass
    checked_years = request.form.getlist("years")
    for i in range(len(checked_years)):
        checked_years[i] = checked_years[i].replace("(", "").replace("'", "").replace(")", "").replace(",", "")

    checked_subjects = request.form.getlist("subjects")
    for i in range(len(checked_subjects)):
        checked_subjects[i] = checked_subjects[i].replace("(", "").replace("'", "").replace(")", "").replace(",", "")
    checked_subjects_ids = db.query(Subject.subject_id).filter(Subject.subject.in_(checked_subjects))
 
    #db.query(Subject.subject_id.filter_by)
    checked_regions = request.form.getlist("regions")
    for i in range(len(checked_regions)):
        checked_regions[i] = checked_regions[i].replace("(", "").replace("'", "").replace(")", "").replace(",", "")

    balls = db.query(sqlalchemy.func.max(TestResult.ball), Student.year, Region.regname, Subject.subject).join(Subject, Subject.subject_id == TestResult.subject_id).join(Student, Student.student_id == TestResult.student_id).join(EducationalOrganization, EducationalOrganization.eo_id == TestResult.eo_id).join(Territory, Territory.territory_id == EducationalOrganization.territory_id).join(Area, Area.area_id == Territory.area_id).join(Region, Region.region_id == Area.region_id).filter(Subject.subject.in_(checked_subjects)).filter(Student.year.in_(checked_years)).filter(Region.regname.in_(checked_regions)).group_by(Student.year, Region.regname, Subject.subject)
    balls = balls.all()
    return render_template("query_result.html", query_res = balls)

if __name__ == '__main__':
    app.run(host="app", port=5555)