from flask import Flask
import threading
import time
app = Flask(__name__)

data_store = {'a': 1}
def interval_query():
    while True:
        global data_store
        time.sleep(1)
	count = data_store['a']
	if count >= 100:
	    count = 1
        vals = {'a': count+1}
	print "setting value"
        data_store.update(vals)

# thread = threading.Thread(name='interval_query', target=interval_query)
# thread.setDaemon(True)
# thread.start()

@app.route('/')
def index():
    return 'Index Page'

@app.route('/jobrunner/v1/health')
def health():
    return '{"status":"Ok"}'

@app.route('/jobrunner/v1/version')
def version():
    return '{"tag":"1","commit":"1","buildId":1}'

@app.route('/random')
def random():
    return str(data_store['a'])

@app.route('/hello')
def hello_world():
    return 'Hello, World!'

def flaskThread():
    app.use_reloader=False
    app.run(host='0.0.0.0', port=5000)
    
def main():
    # app.run(host='0.0.0.0', port=5000, debug=True)
    web = threading.Thread(target=interval_query)
    web.daemon = True
    web.start()
    app.run(host='0.0.0.0', port=5000, debug=True)
    
if __name__ == '__main__':
    main()
