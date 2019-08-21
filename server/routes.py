from flask import jsonify, render_template
from flask import current_app as app


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def main_page(path):
    return render_template('index.html')

# @app.route('/', defaults={'path': ''})
# @app.route('/<path:path>')
# def asdf(path):
#     return str(path)
