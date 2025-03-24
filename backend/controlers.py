# here i am writing all the routes which directs us to web pages
from flask import current_app as app
from flask import Flask, render_template,request,redirect,url_for,session
from backend.models import * # to check the database and match the username and password and other things
# you can name your app as 
# from flask import current_app as ticket_app,,so now you need to write app as ticket app wherever used..
# like ticket_app= Flask(__name__, template_folder="../templates")
# app = Flask(__name__, template_folder="../templates")  # Fix path issue,,sir ne ye line nahi likhi hai
from sqlalchemy import func


@app.route("/" , methods=["GET","POST"])#by default the method is get but if u want to post then u can write post
def login():
    if request.method == "POST":
        username = request.form.get("username")#it is same as username=request.form["username"] the only difference is it don't raise any error if value is missing,,means taking value from form and storing it in variable  name username
        passwd= request.form.get("password")

        #now i want to check whether username and password is present in database or not
        #second thing accordingly i want to redirect this to different html pages...
        usr= Admin_User_Details.query.filter_by(email_username=username,password=passwd).first()# iska matlab hai ki Admin_User_Details table me query karo/search karo,query karni hai ki filter by means search such that email_username=username and password=passwd,give me first record (row) if it is present in database
        if usr and usr.role==0:#saying only if user means if user is existed means it shouldn't be null then execute this code
            
            return redirect(url_for("home"))#if admin exists then render admin home
        elif usr and usr.role==1:
            username=usr.Full_name            
            return redirect(url_for("user_home" , user=username))
        else:
            return render_template("login.html",msg="Invalid Username or Password")
    return render_template("login.html",msg="")# If GET request  show login page,you can write it in the starting of the code also before if statement.

@app.route("/new_registration",methods=["GET","POST"])#listen i can give any name as a route in paranthesis it's not necessary to give name as of html page 
def new_registration():#here i want to submit the data given by user in form in my database also
    if request.method == "POST":
        usr_mail=request.form.get("email_username")#in this variable usr_mail i am storing the value of email_username and name of this variable can be anything
        usr_pass=request.form.get("password")
        usr_name=request.form.get("Full_name")
        usr_qualification=request.form.get("qualification")
        usr_dob=request.form.get("date_of_birth")
        mail=Admin_User_Details.query.filter_by(email_username=usr_mail).first()#to check whether mail given in form by user is present in database or not,if it is present then we will say user already exists...
        if mail:
            return render_template("new_registration.html",msg="User already exists")
        else:
            usr=Admin_User_Details(email_username=usr_mail,password=usr_pass,Full_name=usr_name,qualification=usr_qualification,date_of_birth=usr_dob)#idhar mai ek record/object banake usr naam ka usme batata huu konsa table hai aur konsa column me kya hai
            db.session.add(usr)#This adds a new object (usr) to the database session,It does not yet save the data to the actual database file,
            db.session.commit()#This saves all changes from the session into the database.It makes the changes permanent in the database.
            return render_template("login.html", mesg="Registration Successfull , Login to continue")
    return render_template("new_registration.html")


@app.route("/admin_home")
def home():
    subjects=Subjects.query.all()
    question_counts = {}
    subject=Subjects.query.all()
    chapter=Chapters.query.all()
    for subject in subjects:
        for chapter in subject.chapters_of_a_subject_id:
            count = Questions.query.filter_by(chapter_id=chapter.chapter_id).count()
            question_counts[chapter.chapter_id] = count # Store count for each chapter and creating dictionary
    usr_full_details=Admin_User_Details.query.filter_by(role=0).first()
    admin_name=usr_full_details.Full_name
    return render_template("1_admin_home.html",subjects=subjects,admin=admin_name,question_counts=question_counts)
    

@app.route("/user_home/<string:user>")
def user_home(user):
    subjects=Subjects.query.all()
    question_counts = {}
    subject=Subjects.query.all()
    chapter=Chapters.query.all()
    for subject in subjects:
        for chapter in subject.chapters_of_a_subject_id:
            count = Questions.query.filter_by(chapter_id=chapter.chapter_id).count()
            question_counts[chapter.chapter_id] = count # Store count for each chapter and creating dictionary
    quiz_details=Quiz.query.all()
    return render_template("1_user_home.html",user=user,quizes=quiz_details,question_counts=question_counts)


@app.route("/new_subject" , methods=["GET","POST"])
def new_subject():
    if request.method == "POST":
        sub_name=request.form.get("subject_name")
        discription=request.form.get("discription")
        subject=Subjects.query.filter_by(subject_name=sub_name).first()
        if(sub_name==""):
            return render_template("1a_new_subject.html",msg="bhai koi subject to fill kar lo")
        
        elif subject:
            return render_template("1a_new_subject.html",msg="Subject already exists") 
        else:
            sub=Subjects(subject_name=sub_name,discription=discription)
            db.session.add(sub)
            db.session.commit()
            return redirect(url_for("home"))
    return render_template("1a_new_subject.html")

@app.route("/start_test/<int:quiz_id>/<string:user>",methods=["GET","POST"])
def start_test(quiz_id,user):
    if request.method == "POST":
        user_id=Admin_User_Details.query.filter_by(Full_name=user).first().id
        # scores=Scores.query.filter_by(user_id=user_id).all()
        #total_score=Questions.query.filter_by(quiz_id=quiz_id).count()
        score_id_check=Scores.query.filter_by(quiz_id=quiz_id,user_id=user_id).first()
        if score_id_check:
            #i will update the old marks
            user_id=Admin_User_Details.query.filter_by(Full_name=user).first().id
            score=0
            questions=Questions.query.filter_by(quiz_id=quiz_id).all()
            for question in questions:
                user_answer=request.form.get(str(question.question_id))
                if user_answer==question.correct_option:
                    score=score+1
            quiz_id=quiz_id
            user_id=Admin_User_Details.query.filter_by(Full_name=user).first().id
            #Scores.query.filter_by(quiz_id=quiz_id,user_id=user_id).update({"score":score})
            score=score
            date=Scores.query.filter_by(quiz_id=quiz_id,user_id=user_id).first().date
            no_of_questions=Scores.query.filter_by(quiz_id=quiz_id).first().no_of_questions
            chapter_name=Scores.query.filter_by(quiz_id=quiz_id).first().chapter_name
            score_table=Scores.query.filter_by(quiz_id=quiz_id,user_id=user_id).first()
            score_table.quiz_id=quiz_id
            score_table.user_id=user_id
            score_table.score=score
            score_table.chapter_name=chapter_name
            score_table.date=date
            score_table.no_of_questions=no_of_questions
            db.session.commit()
            return redirect(url_for("score" , user=user))

        else:
            #no.of questions
            no_of_questions = Questions.query.filter_by(quiz_id=quiz_id).count()
            score=0
            quiz_id=quiz_id
            user_id=Admin_User_Details.query.filter_by(Full_name=user).first().id
            questions=Questions.query.filter_by(quiz_id=quiz_id).all()
            chapter_id=Questions.query.filter_by(quiz_id=quiz_id).first().chapter_id
            chapter_name=Chapters.query.filter_by(chapter_id=chapter_id).first().chapter_name
            date=Quiz.query.filter_by(quiz_id=quiz_id).first().date_quiz
            no_of_questions=no_of_questions
           
            for question in questions:
                user_answer=request.form.get(str(question.question_id))
                if user_answer==question.correct_option:
                    score=score+1
            score_obj=Scores(quiz_id=quiz_id,user_id=user_id,score=score,chapter_name=chapter_name,date=date,no_of_questions=no_of_questions)
            db.session.add(score_obj)
            db.session.commit()
            return redirect(url_for("score",user=user))
    question=Questions.query.filter_by(quiz_id=quiz_id).all()
    return render_template("1a_start_test.html" , question=question,user=user,quiz_id=quiz_id)

@app.route("/view_details/<int:chapter_id>/<string:user>")
def view_details(chapter_id,user):
    chapter=Chapters.query.filter_by(chapter_id=chapter_id).first()
    quiz=Quiz.query.filter_by(chapter_id=chapter_id).first()
    subject_id=chapter.subject_id
    subject=Subjects.query.filter_by(subject_id=subject_id).first()
    subject_name=subject.subject_name
    subjects=Subjects.query.all()
    question_counts = {}
    subject=Subjects.query.all()
    chapter=Chapters.query.all()
    for subject in subjects:
        for chapter in subject.chapters_of_a_subject_id:
            count = Questions.query.filter_by(chapter_id=chapter.chapter_id).count()
            question_counts[chapter.chapter_id] = count # Store count for each chapter and creating dictionary
    return render_template("1a_view_details.html",chapter_id=chapter_id,chapter=chapter,quiz=quiz,subject_name=subject_name,user=user,question_counts=question_counts)

@app.route("/new_chapter/<int:subject_id>" ,methods=["GET","POST"])
def new_chapter(subject_id):
    subject=Subjects.query.all()
    id_of_subject=subject_id
    if request.method == "POST":
        chapter_name=request.form.get("chapter_name")
        description=request.form.get("description")
        id_of_subject=request.form.get("subject_id")    
        
        
        chapter=Chapters.query.filter_by(chapter_name=chapter_name).first()
        if(chapter_name==""):
            return render_template("1b_new_chapter.html",msg="Bhai koi chapter fill to kar do" ,  subjects=subject, subject_id=id_of_subject)
        elif chapter:
            return render_template("1b_new_chapter.html",msg="Chapter already exists" ,  subjects=subject, subject_id=id_of_subject)
        else:
            chap=Chapters(chapter_name=chapter_name,description=description,subject_id=id_of_subject)
            db.session.add(chap)
            db.session.commit()
            return redirect(url_for("home"))
    return render_template("1b_new_chapter.html" , msg="",subjects=subject,subject_id=id_of_subject)

@app.route("/admin_quiz",methods=["GET","POST"])
def admin_quiz():
    quiz=Quiz.query.all()
    chapters=Chapters.query.all()
    user=Admin_User_Details.query.filter_by(role=0).first()
    return render_template("2_admin_quiz.html",admin=user.Full_name,quizes=quiz,chapters=chapters)

@app.route("/score/<string:user>")
def score(user):
    user_id=Admin_User_Details.query.filter_by(Full_name=user).first().id
    scores=Scores.query.filter_by(user_id=user_id).all()
    # #date to the quiz id 
    # date={}
    # for score in scores:
    #     date[score.quiz_id]=Quiz.query.filter_by(quiz_id=score.quiz_id).first().date_quiz
    
    # #no.of questions to the quiz id
    # no_of_questions={}
    # for score in scores:
    #     no_of_questions[score.quiz_id]=Questions.query.filter_by(quiz_id=score.quiz_id).count()
    
    #chapter name to the quiz id
    # chapter_name={}
    # for score in scores:
    #     chapter_id=Quiz.query.filter_by(quiz_id=score.quiz_id).first().chapter_id
    #     chapter_name[score.quiz_id]=Chapters.query.filter_by(chapter_id=chapter_id).first().chapter_name
    
    return render_template("2_score.html",user=user,scores=scores)
    
@app.route("/add_question/<int:chapter_id>/<int:quiz_id>",methods=["GET","POST"])
def add_question(chapter_id,quiz_id):
    if request.method == "POST":
        chapter_id=chapter_id
        quiz_id=quiz_id
        question_title=request.form.get("question_title")
        question_statement=request.form.get("question")
        option_a=request.form.get("option_a")
        option_b=request.form.get("option_b")
        option_c=request.form.get("option_c")
        option_d=request.form.get("option_d")
        correct_option=request.form.get("correct_option")
        quest=Questions.query.filter_by(question=question_statement).first()
        if quest:
            return render_template("2a_add_ques.html",msg="Question already exists",chapter_id=chapter_id,quiz_id=quiz_id)
        else:
            question=Questions(chapter_id=chapter_id,quiz_id=quiz_id,question_title=question_title,question=question_statement,option_a=option_a,option_b=option_b,option_c=option_c,option_d=option_d,correct_option=correct_option)
            db.session.add(question)
            db.session.commit()
            return render_template("2_admin_quiz.html",admin=Admin_User_Details.query.filter_by(role=0).first().Full_name,quizes=Quiz.query.all(),chapters=Chapters.query.all())
    return render_template("2a_add_ques.html",chapter_id=chapter_id,quiz_id=quiz_id)

@app.route("/add_newquiz" ,methods=["GET","POST"])
def add_newquiz():
     if request.method == "POST":
        chapter_id=request.form.get("chapter_id")
        date_of_quiz=request.form.get("date_quiz")
        time_of_quiz=request.form.get("time_duration")
        chapter_name=Chapters.query.filter_by(chapter_id=chapter_id).first().chapter_name
        chapter=Quiz.query.filter_by(chapter_id=chapter_id).first()
        if chapter:
            return render_template("2b_add_newquiz.html",msg="Chapter already exists , Go to add question to add question in same chapter",chapter=Chapters.query.all())
        else:
            quiz=Quiz(chapter_id=chapter_id,chapter_name=chapter_name,date_quiz=date_of_quiz,time_duration=time_of_quiz)
            db.session.add(quiz)
            db.session.commit()
            quiz=Quiz.query.all()
            chapters=Chapters.query.all()
            return render_template("2_admin_quiz.html",admin=Admin_User_Details.query.filter_by(role=0).first().Full_name,quizes=quiz,chapters=chapters)
     
     return render_template("2b_add_newquiz.html",chapter=Chapters.query.all())

@app.route("/new_chapter_1" ,methods=["GET","POST"])
def new_chapter_1():
    subject=Subjects.query.all()
    if request.method == "POST":
        chapter_name=request.form.get("chapter_name")
        description=request.form.get("description")
        subject_id=request.form.get("subject_id")
        
        chapter=Chapters.query.filter_by(chapter_name=chapter_name).first()
        if chapter:
            return render_template("1c_new_chapter.html",msg="Chapter already exists" , subjects=subject)
        else:
            chap=Chapters(chapter_name=chapter_name,description=description,subject_id=subject_id)
            db.session.add(chap)
            db.session.commit()
            return redirect(url_for("home"))
    return render_template("1c_new_chapter.html" , msg="",subjects=subject)

@app.route("/search/<string:admin>",methods=["GET","POST"])
def search(admin):
    if request.method == "POST":
        search_txt=request.form.get("search")
        search_of_subject=search_by_subject(search_txt)#searching subjects based on chapter
        search_of_chapter_subject=search_by_chapter(search_txt)
        if search_of_subject:
            subjects=Subjects.query.all()
            question_counts = {}
            subject=Subjects.query.all()
            chapter=Chapters.query.all()
            for subject in subjects:
                for chapter in subject.chapters_of_a_subject_id:
                    count = Questions.query.filter_by(chapter_id=chapter.chapter_id).count()
                    question_counts[chapter.chapter_id] = count # Store count for each chapter and creating dictionary
            usr_full_details=Admin_User_Details.query.filter_by(role=0).first()
            admin_name=usr_full_details.Full_name
            return render_template("1_admin_home.html",subjects=search_of_subject,admin=admin_name,question_counts=question_counts)

        elif search_of_chapter_subject:
            subjects=Subjects.query.all()
            question_counts = {}
            subject=Subjects.query.all()
            chapter=Chapters.query.all()
            for subject in subjects:
                for chapter in subject.chapters_of_a_subject_id:
                    count = Questions.query.filter_by(chapter_id=chapter.chapter_id).count()
                    question_counts[chapter.chapter_id] = count # Store count for each chapter and creating dictionary
            usr_full_details=Admin_User_Details.query.filter_by(role=0).first()
            admin_name=usr_full_details.Full_name
            return render_template("1_admin_home.html",subjects=search_of_chapter_subject,admin=admin_name,question_counts=question_counts)
        else:
            subjects=Subjects.query.all()
            question_counts = {}
            subject=Subjects.query.all()
            chapter=Chapters.query.all()
            for subject in subjects:
                for chapter in subject.chapters_of_a_subject_id:
                    count = Questions.query.filter_by(chapter_id=chapter.chapter_id).count()
                    question_counts[chapter.chapter_id] = count # Store count for each chapter and creating dictionary
            usr_full_details=Admin_User_Details.query.filter_by(role=0).first()
            admin_name=usr_full_details.Full_name
            return render_template("1_admin_home.html",subjects=search_of_subject,admin=admin_name,question_counts=question_counts)

         
    return redirect(url_for("home",admin=admin))


def search_by_subject(search_txt):
    subject_searched=Subjects.query.filter(Subjects.subject_name.contains(search_txt)).all()
    return subject_searched

def search_by_chapter(search_txt):
    subject_searched=Subjects.query.join(Chapters).filter(Chapters.chapter_name.contains(search_txt)).all()
    return subject_searched


@app.route("/edit_subject/<int:subject_id>")
def edit_subject(subject_id):
    subject=Subjects.query.filter_by(subject_id=subject_id).first()
    return render_template("1a_edit_subject.html",subject=subject)

@app.route("/edit_only_subject/<int:subject_id>",methods=["GET","POST"])
def editonly_subject(subject_id):
    if request.method == "POST":
        subject_name=request.form.get("subject_name")
        discription=request.form.get("discription")
        subject=Subjects.query.filter_by(subject_id=subject_id).first()
        subject.subject_name=subject_name
        subject.discription=discription
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("1a_edit_subject.html")



@app.route("/delete_subject/<int:subject_id>")
def delete_subject(subject_id):
    subject=Subjects.query.filter_by(subject_id=subject_id).first()
    db.session.delete(subject)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/edit_chapter/<int:chapter_id>")
def edit_chapter(chapter_id):
    chapter=Chapters.query.filter_by(chapter_id=chapter_id).first()
    return render_template("1b_edit_chapter.html",chapter=chapter)

@app.route("/edit_only_chapter/<int:chapter_id>",methods=["GET","POST"])
def editonly_chapter(chapter_id):
    if request.method == "POST":
        chapter_name=request.form.get("chapter_name")
        description=request.form.get("description")
        chapter=Chapters.query.filter_by(chapter_id=chapter_id).first()
        chapter.chapter_name=chapter_name
        chapter.description=description
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("1b_edit_chapter.html")


@app.route("/delete_chapter/<int:chapter_id>")
def delete_chapter(chapter_id):
    chapter=Chapters.query.filter_by(chapter_id=chapter_id).first()
    db.session.delete(chapter)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/edit_question/<int:question_id>/<int:chapter_id>/<int:quiz_id>" , methods=["GET","POST"])
def edit_question(question_id,chapter_id,quiz_id):
    if request.method == "POST":
        question_title=request.form.get("question_title")
        question_id=question_id
        question=request.form.get("question")
        option_1=request.form.get("option_1")
        option_2=request.form.get("option_2")
        option_3=request.form.get("option_3")
        option_4=request.form.get("option_4")
        correct_answer=request.form.get("correct_answer")
        quest=Questions.query.filter_by(question_id=question_id).first()
        quest.quiz_id=quiz_id
        quest.question_title=question_title
        quest.question=question
        quest.option_1=option_1
        quest.option_2=option_2
        quest.option_3=option_3
        quest.option_4=option_4
        quest.correct_answer=correct_answer
        db.session.commit()
        quiz=Quiz.query.all()
        chapters=Chapters.query.all()
        user=Admin_User_Details.query.filter_by(role=0).first()
        return render_template("2_admin_quiz.html",admin=user.Full_name,quizes=quiz,chapters=chapters)
    question=Questions.query.filter_by(question_id=question_id).first()
    return render_template("2a_edit_question.html",question=question,chapter_id=chapter_id,quiz_id=quiz_id)

@app.route("/delete_question/<int:question_id>")
def delete_question(question_id):
    question=Questions.query.filter_by(question_id=question_id).first()
    db.session.delete(question)
    db.session.commit()
    admin_details=Admin_User_Details.query.filter_by(role=0).first()
    return render_template("2_admin_quiz.html",  quizes=Quiz.query.all(),chapters=Chapters.query.all(), admin=admin_details.Full_name)



@app.route("/delete_quiz/<int:quiz_id>")
def delete_quiz(quiz_id):
    quiz=Quiz.query.filter_by(quiz_id=quiz_id).first()
    db.session.delete(quiz)
    db.session.commit()
    admin_details=Admin_User_Details.query.filter_by(role=0).first()
    return render_template("2_admin_quiz.html",  quizes=Quiz.query.all(),chapters=Chapters.query.all(), admin=admin_details.Full_name)

@app.route("/search_quiz",methods=["GET","POST"])
def search_quiz():
    if request.method == "POST":
        search=request.form.get("search")
        search_of_quiz=Quiz.query.join(Chapters).filter(Chapters.chapter_name.contains(search)).all()#searching the quiz containing quiz name
        quiz=search_of_quiz
        if quiz:
            return render_template("2_admin_quiz.html",  quizes=quiz,chapters=Chapters.query.all(), admin=Admin_User_Details.query.filter_by(role=0).first().Full_name)
        return render_template("2_admin_quiz.html",  quizes=Quiz.query.all(),chapters=Chapters.query.all(), admin=Admin_User_Details.query.filter_by(role=0).first().Full_name)
    return render_template("2_admin_quiz.html",  quizes=Quiz.query.all(),chapters=Chapters.query.all(), admin=Admin_User_Details.query.filter_by(role=0).first().Full_name)


@app.route("/admin_summary/<string:admin>")
def admin_summary(admin):
    return render_template("1_admin_summary.html",admin=admin)


@app.route("/user_summary/<string:user>")
def user_summary(user):
    return render_template("1_user_summary.html",user=user)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('login'))



app.run(debug=True)
