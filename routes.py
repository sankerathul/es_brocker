from flask import Flask, request, jsonify, render_template
from app import get_bucket_aggregate
from flask_cors import CORS

from flask import send_file, send_from_directory, safe_join, abort
from datetime import datetime, timedelta
import time

app = Flask(__name__)
CORS(app,resources={{"origins": "*.*"}})

@app.route('/')
def hello_world():
    return render_template("index.html")

@app.route('/get_data', methods=['POST'])
def get_es_data():
    data = request.json
    try:
        higher_limit = datetime.strptime(data["higher_limit"], '%Y-%m-%d %H:%M:%S.%f')
        lower_limit = datetime.strptime(data["lower_limit"], '%Y-%m-%d %H:%M:%S.%f')

        res,file_name = get_bucket_aggregate(higher_limit, lower_limit)
    except:
        res,file_name = get_bucket_aggregate()
    
    print(file_name)
    download_link = "http://52.56.164.147:3009/get_csv/{}".format(file_name)
    return jsonify({"url":download_link})
    # return res

@app.route("/get_csv/<file_name>")
def get_csv(file_name):
    try:
        return send_file(file_name, as_attachment=True, cache_timeout=0)
    except FileNotFoundError:
        abort(404)

if __name__ == "__main__":
    app.run(host='0.0.0.0')