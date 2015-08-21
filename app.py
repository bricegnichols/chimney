from bottle import route, run, template, static_file
import pandas as pd
import os

@route('/hello')
def hello():
    return "Hello World!" * 3

@route('/test')
def test():
	data_loc = 'task_data.csv'
	df = pd.read_csv(data_loc)

	return df['Task'].iloc[0]

@route('/')
def index():
    global CONFIG
    dir = os.path.dirname(__file__)
    index = open(os.path.join(dir, 'index.html')).read()
    return index

@route('/hello/<name>')
def greet(name='Stranger'):
	return template('Hello {{name}}, how are you?', name=name)

@route('/static/<filepath:path>')
def server_static(filepath):
	return static_file(filepath, root='./static')

run(host='localhost', port=8080, debug=True)