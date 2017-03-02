from flask import Flask
import thread
app = Flask(__name__)

@app.route('/')
def index():
    return 'Index Page'

@app.route('/jobrunner/v1/health')
def health():
    return '{"status":"Ok"}'

@app.route('/jobrunner/v1/version')
def version():
    return '{"tag":"1","commit":"1","buildId":1}'

@app.route('/hello')
def hello_world():
    return 'Hello, World!'

def flaskThread():
    app.run(host='0.0.0.0', port=5000, debug=True)
    
if __name__ == '__main__':
    thread.start_new_thread(flaskThread,())
