from flask import Flask, request, jsonify, render_template
from app import get_bucket_aggregate
from flask_cors import CORS

from flask import send_file, send_from_directory, safe_join, abort
from datetime import datetime, timedelta
import time

from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app,resources={r"/*":{"origins": "*"}})

auth = HTTPBasicAuth()

users = {
    "admin": generate_password_hash("truyu@dashboard"),
}

@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username

@app.route('/')
@auth.login_required
def index():
    return render_template("index.html")

@app.route('/get_data', methods=['POST'])
@auth.login_required
def get_es_data():
    data = request.json
    print("===>", data)
    try:
        higher_limit = datetime.strptime(data["higher_limit"], '%Y-%m-%d %H:%M:%S.%f')
        lower_limit = datetime.strptime(data["lower_limit"], '%Y-%m-%d %H:%M:%S.%f')

        res,file_name = get_bucket_aggregate(higher_limit, lower_limit)
    except:
        res,file_name = get_bucket_aggregate()
    
    # print(file_name)
    download_link = "http://52.56.164.147:3009/get_csv/{}".format(file_name)
    return jsonify({"url":download_link})
    # return res

@app.route("/get_csv/<file_name>")
@auth.login_required
def get_csv(file_name):
    try:
        return send_file(file_name, as_attachment=True, cache_timeout=0)
    except FileNotFoundError:
        abort(404)

if __name__ == "__main__":
    app.run(host='0.0.0.0')