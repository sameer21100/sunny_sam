from flask import Flask,redirect,url_for,render_template, request, session, flash
# we use request to get the data from the frontEnd
from datetime import timedelta
# to create a session lifetime 


app=Flask(__name__)
app.secret_key="Hello warld"
app.permanent_session_lifetime=timedelta(minutes=20)
# minutes=5

##Pass a value from backend to front end using render_template
@app.route("/")
def main():
    return render_template("login.html")
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
        fname=request.form["fname"]
        mail=request.form["gmail"]
        session["user"]=fname
        session["gmail"]=mail
        flash("You are now logged in")
        return redirect(url_for("user"))    
        # return redirect(url_for("home",name=fname)) this just simply sends the front end data to backend and redirects to a page
    else:
        if "user" in session:
            return redirect(url_for("user"))

        return render_template("login.html")
@app.route("/user")
def user():
    session.permanent=True
    if "user" in session:
        user=session["user"]
        gmail=session["gmail"]
        return render_template("user.html",user=user,gmail=gmail)
    else:
        flash("You need to login first","info")
        return redirect(url_for("login"))
#To remove all the stored session history, session is like a dictionary.
@app.route("/logout")
def logout():
    session.pop("user",None)
    session.pop("gmail",None)
    return redirect(url_for("login"))

if(__name__)=="__main__":
    app.run(debug=True) #to allow the changes made to automatically reflect on to the website