from flask import Flask,redirect,url_for,render_template, request, session, flash
# we use request to get the data from the frontEnd
from datetime import timedelta
# to create a session lifetime 
from flask_sqlalchemy import SQLAlchemy



app=Flask(__name__)
app.permanent_session_lifetime=timedelta(minutes=20)
# minutes=5
app.secret_key="Hello warld"
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///users.sqlite3.' #users is the name of the object(table) that we are creating
db=SQLAlchemy(app)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False

class users(db.Model):
    _id=db.Column("id",db.Integer,primary_key=True)
    name=db.Column(db.String(100))
    email=db.Column(db.String(100))
    animal=db.Column(db.String(50))
    def __init__(self,name,email,animal):
        self.name=name
        self.email=email
        self.animal=animal
##Pass a value from backend to front end using render_template
@app.route("/")
def main():

    return render_template("index.html")
@app.route("/<name>")# write any route to access this route.here name is the name of variable 
def home(name): ### we can return an html tag or html page or simple text;
    # return render_template("index.html", content=name, admin='string or name or any variable')   #  content and admin are the variables which can be accessed in html
    return render_template("index.html",names=name,content=['Steal','Resources','using','web','dev'])#sent html page as well as the variables which can be accessed in frontend;
# @app.route("/profile/")
# def profile():
#     return "working"









# @app.route("/<page>")### simply if the user inputs the wrong endpoint 
# def error(page):
#     # print("ha") printed in terminal
#     return  redirect(url_for("home1",name="rnad"))  ##cannot pass the variable inside the redirect only strings allowed
# @app.route("/home1/")
# def home1(name):
#     return  f"helo betc {name}" ##url for home instead of "/"

@app.route("/login",methods=["POST","GET"])
def login():
    if request.method=="POST":
        fname=request.form["fname"].strip()
        mail=request.form["gmail"].strip()
       
        query=users.query.filter_by(name=fname, email=mail).first()
        if  query :
            session["user"]=query.name
            session["gmail"]=query.email
            session["animal"]=query.animal
            flash(f"Welcome back")
        else:
            flash("Provide correct email or signup ")
            return redirect(url_for("login"))
            # usr_obj=users(fname,mail,"")
            # db.session.add(usr_obj)
            # db.session.commit()
        #These three lines are used to add the data to the database and commit the changes done to the database

        flash("You are now logged in")
        session.permanent=True
        return redirect(url_for("user"))    
        # return redirect(url_for("home",name=fname)) this just simply sends the front end data to backend and redirects to a page
    else:
        if "user" in session:
            flash("You are already logged in","danger")
            return redirect(url_for("user"))

        return render_template("login.html")
@app.route("/user",methods=["POST","GET"])
def user():
    name=session["user"]
    mail=session["gmail"]
    animal=None
    if request.method =="POST":
        form_type=request.form.get("form_type")
        if form_type=="update_animal":
            flash("Janawar's name has been updated")
            animal=request.form["animal"]
            session["animal"]=animal
            name=session["user"]
            usr_obj=users.query.filter_by(name=name).first()
            usr_obj.animal=animal
            gmail=usr_obj.email
            # print(usr_    obj.animal)
            db.session.commit()
            return redirect(url_for("user"))
            
        elif form_type=="update_email":
            flash("Email chanded succussfully")
            gmail=request.form["email"]
            session["gmail"]=gmail
            fname=session["user"]
            usr_obj=users.query.filter_by(name=fname).first()
            usr_obj.email=gmail
            db.session.commit()
            return redirect(url_for("user"))
    if "user" in session:
        usr_obj=users.query.filter_by(name=name,email=mail).first()
        animal=usr_obj.animal
        gmail=usr_obj.email

        # animal=session["animal"]
        return render_template("user.html",user=user,email=gmail,animal=animal)
    else:
        flash("You need to login first","info")
        return redirect(url_for("login"))
    
@app.route("/clean_data")
def clean():
    usr_obj=users.query.all()
    seen=set()
    to_del=[]
    for user in usr_obj:
        identifier=user.name.strip().lower()+"#@#"+user.email.strip().lower()
        if identifier in seen:
            to_del.append(user)
        else:
            seen.add(identifier)
    for user in to_del:
        db.session.delete(user)
    db.session.commit()
    if len(to_del)==0:
        return f"No users were duplicate"
    return f"Removed users are {len(to_del)} in nuumber"
    
@app.route("/view")
def view():
    if "user" in session:
        return render_template("view.html", values=users.query.all())
    else:
        flash("Please login first")
        return redirect(url_for("login"))

@app.route("/signup", methods=["POST","GET"])
def signup():
    if request.method=="POST":
        name=request.form["name"]
        email=request.form["email"]
        query=users.query.filter_by(name=name, email=email).first()
        if query:
            flash("This user already exits try to login")
        else:
            usr_obj=users(name,email,"")
            db.session.add(usr_obj)
            db.session.commit()
            flash("Account create successfully")
        return redirect(url_for("login"))
    return render_template("signup.html")
#To remove all the stored session history, session is like a dictionary.
@app.route("/logout")
def logout():
    if "user" in session:
        user=session["user"]
        session.pop("user",None)
        session.pop("gmail",None)
        session.pop("animal",None)
        flash(f"The user {user} has been logged out successfully")
        
    else:
        flash("Please Login kar pehle")
    return redirect(url_for("login"))

if(__name__)=="__main__":
    with app.app_context():
        db.create_all()#create database if it doesn't already exists.,above the app.run so that app dosen't give error referrring to db
    app.run(debug=True) #to allow the changes made to automatically reflect on to the website