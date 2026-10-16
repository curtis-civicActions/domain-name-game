import os
from flask import Blueprint, jsonify, request
from flask import render_template, current_app
from app.services.datagenerator import DataGenerator
from app.services.datamanager import DataManager
from app.services.question_cache import question_cache
from app.services.aihintservices import AIHintService
from app.forms import UserForm


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

@bp.route("/gather/data")
def gather_data():
    return render_template('pages/gather.html')

@bp.route("/get-partial/question/<view_name>")
def get_partial(view_name):
    datamanager = DataManager()
    tempdata = datamanager.getQuestion(view_name)
    show_hint = current_app.config.get("AI_HINT_ENABLED", False)
    if isinstance(show_hint, str):
        show_hint = show_hint.lower() == "true"

    print(show_hint)
    # Map the URL parameter to the corresponding partial template.
    safe_view_name = os.path.basename("question")
    return render_template(f'partials/{safe_view_name}.html', data=tempdata, show_hint=show_hint)

@bp.route("/fetch/data")
def fetch_data():
    data_generator = DataGenerator()

    # Retain ability to show the data that was loaded.
    data_to_display = data_generator.generate_data("external", True)

    return jsonify({
        "success": True,
        "message": "Data has been successfully loaded into database.",
    })

@bp.route("/load/data", methods = ["GET", "POST"])
def load_data():
    form = UserForm(request.form if request.method == 'POST' else None)
    message = None

    if request.method == 'POST':
        form.domains.entries.pop()
        if form.validate():
            # Access the submitted data as a Python list
            submitted_domains = form.domains.data
            clean_domains = [d for d in submitted_domains  if d.strip()]

            datamanager = DataManager()
            dm_response = datamanager.insertdata({"name": form.name.data, "domains": clean_domains})
            message = dm_response["message"]

            if dm_response["status"]:
                form = UserForm(formdata=None)

    elif request.method == 'GET':
        pass
    else:
        pass

    return render_template('pages/loaddata.html', form=form, message=message)

@bp.route("/validate-field", methods=["POST"])
def validate_field():

    form = UserForm(request.form)
    list_name = request.form.get("_list_name")
    raw_index = request.form.get("_index")

    if not list_name or raw_index is None or not hasattr(form, list_name):
        return jsonify({"_valid": False, "_error": ['Invalid field or list name']}), 400

    try:
        index = int(raw_index)
    except ValueError:
        return jsonify({"_valid": False, "_error": ['Index must be an integer']}), 400

    field_list = getattr(form, list_name)

    if index < 0 or index >= len(field_list):
        return jsonify({"_valid": False, "_error": ['Index of field mismatch']}), 400

    # Locate the specific subfield entry using the integer index
    target_entry = field_list[int(index)]
    is_valid = target_entry.validate(form)

    response_payload = jsonify({
        '_valid': is_valid,
        '_error': target_entry.errors,
        '_element': f"{list_name}-{index}"
    })
    return response_payload

@bp.route("/hint", methods = ["GET","POST"])
def get_hint():
    question_id = request.form.get("question_id")
    question = question_cache.get(question_id)

    if not question_id:
        return jsonify({"Success": False, "message": "Missing question id."})

    hint_service = AIHintService()
    hint = hint_service.generate_hint(question)
    return hint