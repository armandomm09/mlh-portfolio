import os
import datetime
import sqlite3
from flask import Flask, render_template, request
from dotenv import load_dotenv
from peewee import *
from playhouse.shortcuts import model_to_dict

# Configure SQLite datetime adapter to avoid deprecation warning
def adapt_datetime(val):
    return val.isoformat()

def convert_datetime(val):
    return datetime.datetime.fromisoformat(val.decode())

sqlite3.register_adapter(datetime.datetime, adapt_datetime)
sqlite3.register_converter("datetime", convert_datetime)

load_dotenv()
app = Flask(__name__)

if os.getenv('TESTING') == 'true':
    print('Running in test mode')
    mydb = SqliteDatabase('file:memory?mode=memory&cache=shared', uri=True)
else:
    mydb = MySQLDatabase(
    os.getenv("MYSQL_DATABASE"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    host=os.getenv("MYSQL_HOST"),
    port=3306,
)



print(mydb)


class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb


mydb.connect()
mydb.create_tables([TimelinePost])


@app.route('/api/timeline_post', methods=['POST'])
def timeline_post():
    name = request.form['name']
    email = request.form['email']
    content = request.form['content']
    
    # Validate required fields
    if not name:
        return "Invalid name", 400
    
    if not content:
        return "Invalid content", 400
    
    # Basic email validation
    if not email or '@' not in email or '.' not in email:
        return "Invalid email", 400
    
    timeline_post = TimelinePost.create(name=name, email=email, content=content)
    return model_to_dict(timeline_post)

@app.route('/api/timeline_post', methods=['GET'])
def get_timeline_post():
    return {
        'timeline_posts': [
            model_to_dict(p)
            for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
            ]
    }
    

@app.route('/')
def index():
    return render_template('index.html', title="Armando Mac Beath", url=os.getenv("URL"))

@app.route('/timeline')
def timeline():
    return render_template('timeline.html', title="Timeline", url=os.getenv("URL"))

# Hobbies route which returns the hobbies html page
@app.route('/hobbies')
def hobbies():
    return render_template('hobbies.html', title="Our Hobbies", url=os.getenv("URL"))

#Route for work experience page
@app.route('/work')
def work():
    return render_template('workExperience.html', title="Work Experience", url=os.getenv("URL"))

# About us route which returns the about us html page
@app.route('/about')
def about():
    return render_template('aboutUs.html', title="About Us", url=os.getenv("URL"))

#Route for education page
@app.route('/education')
def education():
    # Create a dictionary with education data for each person
    education_data = {
        "Armando": [
            {
                "degree": "Primary School",
                "institution": "Andes International School",
                "dates": "2010 - 2016",
                "description": "School with an international curriculum.",
                "icon": "fas fa-school"
            },
            {
                "degree": "Middle School Diploma",
                "institution": "Andes International School",
                "dates": "2016 - 2019",
                "description": "Graduated with honors. ",
                "icon": "fas fa-school"
            },
            {
                "degree": "High School Diploma",
                "institution": "Prepa Tec Campus Puebla",
                "dates": "2018 - 2021",
                "description": "Program of international baccalaureate.",
                "icon": "fas fa-school"
            },
            {
                "degree": "B.S. in Mechatronics Engineering",
                "institution": "Tecnológico de Monterrey, Campus Puebla",
                "dates": "2021 - 2025",
                "description": "Specializing in automation and robotics. Lead programmer for the FRC team.",
                "icon": "fas fa-graduation-cap"
            }
        ]
    }
    # Render the education template with the education data
    return render_template('education.html', education_data=education_data)

# map route which returns the map html page
@app.route('/map')
def map():
    return render_template('map.html', title="Places we've been", url=os.getenv("URL"))

