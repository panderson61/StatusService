from flask import Flask
from flask import render_template, request, redirect, url_for, session, abort, flash
import threading
import logging
import time
import os
app = Flask(__name__)

data_store = {'a' : 1, 'b' : 88}
run = False
inc = None
dec = None

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
def default():
    logging.debug("running default")
    if session.get('logged_in'):
        return render_template('index.html')
    return render_template('login.html')

@app.route('/home')
def home():
    logging.debug("running home")
    return redirect(url_for('default'))

@app.route('/index',methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        # len = request.headers["Content-Length"]
        # data=request.stream.read()
	# logging.debug(data)
	result_dict = request.form.to_dict()
	logging.debug(result_dict)
        if result_dict['StopButton'] == 'Stop':
	    logging.debug("Stop button pressed")
            return redirect(url_for('stop'))
        elif result_dict['StopButton'] == 'Start':
	    logging.debug("Start button pressed")
            return redirect(url_for('start'))
        elif result_dict['StopButton'] == 'Logout':
	    logging.debug("Logout button pressed")
            return redirect(url_for('logout'))
        else:
	    logging.debug("nothing happened")
    elif request.method == 'GET':
	logging.debug("returning the index page")
    return redirect(url_for('default'))

@app.route('/login', methods=['POST', 'GET'])
def do_admin_login():
    logging.debug("running login")
    if request.method == 'POST':
        if request.form['password'] == 'password' and request.form['username'] == 'admin':
            session['logged_in'] = True
        else:
            flash('wrong password!')
    return redirect(url_for('default'))

@app.route('/logout')
def logout():
    logging.debug("running logout")
    session['logged_in'] = False
    return redirect(url_for('default'))

@app.route('/jobrunner/v1/health')
def health():
    logging.debug("running health")
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
    logging.debug("running hello_world")
    return 'Hello, World!'

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    logging.debug("running hello template")
    return render_template('hello.html', name=name)

@app.route('/start')
def start():
    global run
    global dec
    global inc
    logging.debug("running start")
    if not session.get('logged_in'):
        return redirect(url_for('default'))
    run = True

    if inc is None:
        logging.info("Starting inc thread")
        inc = threading.Thread(target=incrementer)
        inc.daemon = True
        inc.start()
    else:
        logging.info("inc thread already running")

    if dec is None:
        logging.info("Starting dec thread")
        dec = threading.Thread(target=decrementer)
        dec.daemon = True
        dec.start()
    else:
        logging.info("dec thread already running")
    return redirect(url_for('default'))

@app.route('/stop')
def stop():
    global run
    global dec
    global inc
    logging.debug("running stop")
    if not session.get('logged_in'):
        return redirect(url_for('default'))
    run = False
    if inc is not None:
        inc.join()
        inc = None
    if dec is not None:
        dec.join()
        dec = None
    return redirect(url_for('default'))

def main():
    logging.basicConfig(filename='/var/log/statusservice.log',level=logging.DEBUG)
    #my_logger = logging.getLogger('MyLogger')
    #my_logger.setLevel(logging.DEBUG)
    #log_handler = logging.handlers.SysLogHandler(address='/var/log/statusservice.log')
    #my_logger.addHandler(log_handler)

    logging.info("Starting app")
    app.secret_key = os.urandom(12)
    app.run(host='0.0.0.0', port=5000, debug=True)
    
if __name__ == '__main__':
    main()
