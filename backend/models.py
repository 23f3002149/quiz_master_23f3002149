# here i am writing the data models.
#here we are going to create all data models with all the relationship ofprimary key and all other stuff

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()#here i am creating instance(object) of the database , Creating an instance of the database means setting up and initializing a specific database that can be used for storing and managing data.
#In practical terms, it refers to:

# Establishing a Connection: Connecting your application to a database server (e.g., SQLite, MySQL, PostgreSQL).
# Creating Database Objects: Defining tables, columns, relationships, and constraints.
# Allocating Storage: Setting up space in memory or disk for storing data.
# Initializing with Data (Optional): Pre-populating tables with required records (e.g., adding an admin user by default).

# creating first entity(first_table)
# class User(db.Model): Defines a table named user.
# db.Column(...): Defines columns in the table.
#db = SQLAlchemy(app) you will write this if and only if models.py is combined in app.py
class Admin_User_Details(db.Model):
    __tablename__ = 'admin_user_details'
    id=db.Column(db.Integer, primary_key=True,autoincrement=True)#Ensures that the ID column automatically increments for each new row inserted into the table.It applies only to integer primary keys.The database automatically assigns a new unique ID starting from 1 and increases by 1 for each new entry.
    email_username = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)#not neccessary to be unique# here string(120) means 120 characters
    Full_name = db.Column(db.String(80), nullable=False)#not neccessary to be unique
    qualification=db.Column(db.String(80), nullable=False)#not neccessary to be unique
    #date_of_birth=db.Column(db.Date, nullable=False)#not neccessary to be unique
    date_of_birth=db.Column(db.String(80), nullable=False)#not neccessary to be unique
    role = db.Column(db.Integer, nullable=False, default=1)#remember this only the first user with register through this register form,admins will have to register in db browser manually or using insert command of sql 
   # relations with other tables(backrefrencing means getting all child infromation through parent )we will write later,,,,haaa now it is written below
    #now through user id we want to get all the details of scores of that user id
    scores_of_a_userid = db.relationship('Scores', cascade='all, delete', backref='admin_user_details', lazy=True)#name of the backrefrence is scores_of_a_userid#we say this is linked to the scores table#cascade means if a id gets deleted here delete all the data of scores linked to that id#backref=admin_user_details means the current table or the table to which it is backrefrencing#loading style is lazy()
   #cascade means if master is removed all the child will get removed
#creating 2nd entity(second_table)(subjects)
class Subjects(db.Model):
    __tablename__ = 'subjects'
    subject_id=db.Column(db.Integer, primary_key=True,autoincrement=True)#iska student id se kuch lena dena nahi hai
    subject_name=db.Column(db.String(80), nullable=False,unique=True)
    discription=db.Column(db.String(300), nullable=False)
    #relations with other tables(foreign key)we will write later,,haaa now it is written below
    chapters_of_a_subject_id = db.relationship('Chapters', cascade='all, delete', backref='subjects', lazy=True)# it tells all the chapters of a subject(here we are getting suject through subject id)

#creating 3rd entity(third_table)(chapters)
class Chapters(db.Model):
    __tablename__ = 'chapters'
    chapter_id=db.Column(db.Integer, primary_key=True,autoincrement=True)#iska student id se kuch lena dena nahi hai
    chapter_name=db.Column(db.String(80), nullable=False,unique=True)
    description=db.Column(db.String(300), nullable=False)
    subject_id=db.Column(db.Integer, db.ForeignKey('subjects.subject_id'), nullable=False)
    #we can have subject name also in this table but it should be a foreign key(primary key of subjects table),that's why we include subject_id in this table
    #relations with other tables(foreign key)we will write later,,haaa now it is written below
    quizzes_of_a_chapter_id = db.relationship('Quiz', cascade='all, delete', backref='chapters', lazy=True)# it tells all the quizzes of a chapter(here we are getting chapter through chapter id)
    #here cascade all delete means if a chapter is deleted all the quizzes linked to that chapter will get deleted
    questions_of_a_chapter_id = db.relationship('Questions', cascade='all, delete', backref='chapters', lazy=True)# it tells all the questions of a chapter(here we are getting chapter through chapter id)
    #here cascade all delete means if a chapter is deleted all the questions linked to that chapter will get deleted

#creating 4th entity(fourth_table)(Quiz)
class Quiz(db.Model):#class name should start with capital letter,tablename should start with small letter
    __tablename__ = 'quiz'
    quiz_id=db.Column(db.Integer, primary_key=True,autoincrement=True)#iska student id se kuch lena dena nahi hai
    chapter_id=db.Column(db.Integer, db.ForeignKey('chapters.chapter_id'), nullable=False)
    #we can have chapter name also in this table but it should be a foreign key(primary key of chapters table),that's why we include chapter_id in this table
    #date_quiz=db.Column(db.Date, nullable=False)
    date_quiz=db.Column(db.String(80), nullable=False)
    #time_duration=db.Column(db.Interval, nullable=False)
    time_duration=db.Column(db.Integer, nullable=False)
    chapter_name=db.Column(db.String(80) , nullable=False)#remember it has relationship with chapters tables as of chapter_name
    #relations with other tables(foreign key)we will write later,,haa now it is written below
    questions_of_a_quiz_id = db.relationship('Questions', cascade='all, delete', backref='quiz', lazy=True)# it tells all the questions of a quiz(here we are getting quiz through quiz id)
    #here cascade all delete means if a quiz is deleted all the questions linked to that quiz will get deleted
    # it tells all the scores(scores of evry user given the quiz) of a quiz(here we are getting quiz through quiz id)
    #here cascade is not applied because suppose a quiz is delted then those who gave it previously their record should not be deleted...
#creating 5th entity(fifth_table)(Questions)
class Questions(db.Model):
    __tablename__ = 'questions'
    question_id=db.Column(db.Integer, primary_key=True,autoincrement=True)#iska student id se kuch lena dena nahi hai
    chapter_id=db.Column(db.Integer, db.ForeignKey('chapters.chapter_id'), nullable=False)
    quiz_id=db.Column(db.Integer, db.ForeignKey('quiz.quiz_id'), nullable=False)
    question_title=db.Column(db.String(80), nullable=False)
    question=db.Column(db.String(300), nullable=False)
    option_a=db.Column(db.String(300), nullable=False)
    option_b=db.Column(db.String(300), nullable=False)
    option_c=db.Column(db.String(300), nullable=False)
    option_d=db.Column(db.String(300), nullable=False)
    correct_option=db.Column(db.String(300), nullable=False)
    #relations with other tables(foreign key)we will write later,,,haaa now it is written below
    #it's a child table only not a parent table so no relationship of backrefrence is defined here
    
#creating 6th entity(sixth_table)(Scores)
class Scores(db.Model):
    __tablename__ = 'scores'
    score_id=db.Column(db.Integer, primary_key=True,autoincrement=True)#iska student id se kuch lena dena nahi hai
    quiz_id=db.Column(db.Integer, nullable=False)
    user_id=db.Column(db.Integer, db.ForeignKey('admin_user_details.id'), nullable=False)
    score=db.Column(db.Integer, nullable=False)
    chapter_name=db.Column(db.String(80) , nullable=False)
    date=db.Column(db.String(80), nullable=False)  # Auto-save current date
    no_of_questions=db.Column(db.Integer, nullable=False)
    #db.ForeignKey('quiz.quiz_id')from line no. 128
    #relations with other tables(foreign key)we will write later,haaa now it is written below
    #it's a child table only not a parent table so no relationship of backrefrence is defined here
    #Specific Time (like alarm)	db.Time	14:30:00
    #Timer Duration (countdown, elapsed time)	db.Interval	2:30:00 (2 hours 30 min)
    #Timestamp (start/end time)	db.DateTime	2025-02-05 14:30:00
    #Date (start/end date)	db.Date	2025-02-05
























# db = SQLAlchemy(app): Creates an instance of the database.
# db.create_all(): Generates the database schema (tables, relationships).