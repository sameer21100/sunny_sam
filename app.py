from flask import Flask,redirect,url_for

app=Flask(__name__)
@app.route("/")
def home(): ### we can return an html tag or html page or simple text;
    return "Main page in progress:"
@app.route("/<page>")### simply if the user inputs the wrong endpoint 
def error(page):
    return f"The {page} page does not exists"
@app.route("/home1")
def home1():
    return redirect(url_for("home")) ##url for home instead of "/"

if(__name__)=="__main__":
    app.run()