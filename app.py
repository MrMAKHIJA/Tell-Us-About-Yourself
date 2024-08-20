from flask import Flask, request, jsonify
from functools import wraps
import json

app = Flask(__name__)

# Basic authentication decorator
def check_auth(username, password):
    return username == 'your_username' and password == 'your_password'

def authenticate():
    return jsonify({"message": "Authentication required"}), 401

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    with open('data.json', 'w') as f:
        json.dump(data, f)
    return jsonify({"message": "Data saved successfully!"})

@app.route('/view', methods=['GET'])
@requires_auth
def view():
    with open('data.json', 'r') as f:
        data = json.load(f)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
