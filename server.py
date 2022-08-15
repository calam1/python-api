from flask import Flask
from flask import send_from_directory 
from flask import request

# import time
import sys

app = Flask(__name__)

@app.route('/index')
def get():
    sys.stderr.write("headers: " + str(request.headers) + "\n")
    return 'hello'

@app.route('/health-check')
def getHealthCheck():
    return 'UP'

@app.route("/static/<name>")
def download_file(name):
    return send_from_directory(
        'static', name, as_attachment=True
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', threaded = True)
    
