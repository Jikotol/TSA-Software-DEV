from flask import Blueprint, render_template

# set name same as file name and var name
second = Blueprint("second", __name__, static_folder="static", template_folder="templates")

@second.route("/home")
@second.route("/")
def home():
    return render_template("home.html")
