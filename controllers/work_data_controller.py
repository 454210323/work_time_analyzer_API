from flask import (
    Blueprint,
    jsonify,
    request,
    send_file,
    Flask,
    flash,
    redirect,
    url_for,
    current_app,
)
from werkzeug.utils import secure_filename
from services import work_data_service
import os

bp_work_data = Blueprint("work_data", __name__, url_prefix="/work_data")

@bp_work_data.route("/month/<string:user_id>/<string:date_str>", methods=["GET"])
def get_work_data_by_month_and_user(user_id, date_str):
    data = work_data_service.get_work_data_by_month_and_user(user_id, date_str)
    return jsonify(data), 200


@bp_work_data.route("/month", methods=["GET"])
def get_work_data_by_month_and_team():
    data = request.args.to_dict()
    data = work_data_service.get_work_data_by_month_and_team(data)
    return jsonify(data), 200


@bp_work_data.route("/month/excel", methods=["GET"])
def get_work_data_by_month_and_team_excel():
    data = request.args.to_dict()
    file_name = work_data_service.generate_work_data_excel(data)
    return send_file(file_name, as_attachment=True), 200


@bp_work_data.route("/day/<string:user_id>/<string:date_str>")
def get_work_data_by_day_and_user(user_id, date_str):
    data = work_data_service.get_work_data_by_day_and_user(user_id, date_str)
    return jsonify(data), 200


@bp_work_data.route("", methods=["POST"])
def add():
    data = request.json
    result = work_data_service.add_work_data(data)
    return jsonify(result), 200


@bp_work_data.route("", methods=["PUT"])
def modify():
    data = request.json
    result = work_data_service.modify_work_data(data)
    return jsonify(result), 200


@bp_work_data.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return "No file part"
    file = request.files["file"]
    if file.filename == "":
        return "No selected file"
    # file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
    file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename))
    work_data_service.parse_upload_file(file)
    return "upload successfully"
