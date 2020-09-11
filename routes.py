from flask import Flask
from app import get_bucket_aggregate


app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/get_data')
def get_es_data():
    res = get_bucket_aggregate()
    print(res)
    return res

if __name__ == "__main__":
    app.run(host='0.0.0.0')