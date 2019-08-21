import os, datetime
import requests
import hashlib

from flask import jsonify, render_template, Response
from flask import current_app as app

FILE_PATH = os.path.dirname(os.path.abspath(__file__))
CACHE_PATH = os.path.join(FILE_PATH, "apicache")

@app.route('/apicache/<path:path>')
def apicache(path):
    try:

        resulttext = ""
        resultstatus = 500
        
        cachefile = hashlib.sha256(path.encode()).hexdigest() + ".cache"
        cachefile = os.path.join(CACHE_PATH, cachefile)
        

        if os.path.isfile(cachefile):
            cachetime = datetime.datetime.fromtimestamp(os.path.getmtime(cachefile))

            if cachetime > datetime.datetime.now() - datetime.timedelta(days=1):
                with open(cachefile, 'r') as fp:
                    resulttext = fp.read()
                    resultstatus = 200
                    res = Response(response=resulttext, status=resultstatus, mimetype="application/xml")
                    res.headers["Content-Type"] = "text/xml; charset=utf-8"
                    return res

        

        r = requests.get("http://api.korea.go.kr/openapi/" + path)
        resulttext = r.text
        resultstatus = r.status_code


        with open(cachefile, "w") as fp:
            fp.write(resulttext)
        

        res = Response(response=resulttext, status=resultstatus, mimetype="application/xml")
        res.headers["Content-Type"] = "text/xml; charset=utf-8"
        return res
    except Exception as err:
        return str(err), 500


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def main_page(path):
    return render_template('index.html')

