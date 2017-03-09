from flask import Flask
from flask import render_template
import threading
import logging
import time
app = Flask(__name__)

data_store = {'a' : 1, 'b' : 88}
run = False
def incrementer():
    global run
    global data_store
    while run:
        time.sleep(5)
	count = data_store['a']
	if count >= 100:
	    count = 1
        vals = {'a': count+1}
	logging.debug("inc count is %s", count)
        data_store.update(vals)

def decrementer():
    global run
    global data_store
    while run:
        time.sleep(7)
	count = data_store['b']
	if count <= 1:
	    count = 100
        vals = {'b': count-1}
	logging.debug("dec count is %s", count)
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
    return ('a=' + str(data_store['a']) + ', b=' + str(data_store['b']))

@app.route('/hello')
def hello_world():
    return 'Hello, World!'

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

@app.route('/stop')
def stop():
    global run
    run = False
    return 'stopping'

def main():
    global run
    run = True
    logging.basicConfig(filename='/var/log/flask.log',level=logging.DEBUG)

    logging.info("Starting inc thread")
    inc = threading.Thread(target=incrementer)
    inc.daemon = True
    inc.start()

    logging.info("Starting dec thread")
    dec = threading.Thread(target=decrementer)
    dec.daemon = True
    dec.start()

    logging.info("Starting app")
    app.run(host='0.0.0.0', port=5000, debug=True)
    
if __name__ == '__main__':
    main()
