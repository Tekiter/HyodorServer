from flask import jsonify
from flask import current_app as app

@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pongpong!')


@app.route('/')
def main_page():
    return "This is SecureSW API Server"