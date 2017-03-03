from flask import Flask
import threading
import logging
import time
app = Flask(__name__)

data_store = {'a': 1}
def incrementer():
    while True:
        global data_store
        time.sleep(1)
	count = data_store['a']
	if count >= 100:
	    count = 1
        vals = {'a': count+1}
	logging.debug("count is %s", count)
        data_store.update(vals)

@app.route('/')
def index():
    return 'Index Page'

@app.route('/jobrunner/v1/health')
def health():
    return '{"status":"Ok"}'

@app.route('/jobrunner/v1/version')
def version():
    return '{"tag":"1","commit":"1","buildId":1}'

@app.route('/value')
def value():
    logging.debug("running value")
    return str(data_store['a'])

@app.route('/hello')
def hello_world():
    return 'Hello, World!'

def main():
    logging.basicConfig(filename='/var/log/flask.log',level=logging.DEBUG)

    logging.info("Starting counter thread")
    web = threading.Thread(target=incrementer)
    web.daemon = True
    web.start()
    logging.info("Starting app")
    app.run(host='0.0.0.0', port=5000, debug=True)
    
if __name__ == '__main__':
    main()
