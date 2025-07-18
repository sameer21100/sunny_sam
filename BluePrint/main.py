from flask import render_template,Flask
from packages.flower import flower
app=Flask(__name__)
app.register_blueprint(flower,prefix_url="")
@app.route("/")
def test():
    return "<h1> test</h1>"


if(__name__)=="__main__":
    app.run(debug=True)
