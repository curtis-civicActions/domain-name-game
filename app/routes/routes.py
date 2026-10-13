import os
from flask import Blueprint
from flask import render_template
from app.services.datagenerator import DataGenerator
from app.services.datamanager import DataManager

bp = Blueprint("main", __name__)

# Sample backend state variable
toggle_state = {"active": False}

@bp.route("/")
def home_page():
    return render_template("pages/home.html")

@bp.route("/about")
def about():
    return render_template("pages/about.html")

@bp.route("/start")
def start():
    return render_template("pages/start.html", is_active=toggle_state["active"])

@bp.route("/get-partial/question/<view_name>")
def get_partial(view_name):
    datamanager = DataManager()
    tempdata = datamanager.getQuestion(view_name)
    # Map the URL parameter to the corresponding partial template.
    safe_view_name = os.path.basename("question")
    return render_template(f'partials/{safe_view_name}.html', data=tempdata)

@bp.route("/fetch/data")
def fetch_data():
    data_generator = DataGenerator()
    data_to_display = data_generator.generate_data("external", True)
    return render_template('pages/datadisplay.html', data=data_to_display)
