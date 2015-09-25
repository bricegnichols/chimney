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

# Should we use the route as a list of queries?
# e.g., /1/3/4 represents the cost, time, and priority values?
# Python could parse those values and use them to query the csv data

@route('/<filepath:path>')
def query_data(filepath):
	# assuming the query_string is defined as:
	# /cost/priority/time
	cost = filepath.split('/')[0]
	priority = filepath.split('/')[1]
	time = filepath.split('/')[2]
	

	return filter_data(cost, time, priority)

	## return 'hey guys' + cost + time + priority

def filter_data(cost, time, priority):
	data_loc = 'task_data.csv'
	df = pd.read_csv(data_loc)
	print cost
	a = df.query('Cost <= ' + str(cost) + ' & ' + 'Time <= ' + str(time) + ' & ' + 'Priority <= ' + str(priority))
	#return str(a)
	#return "Cost: " + cost + "," + "priority: " + priority
	return a.to_html(classes='my_class')

run(host='localhost', port=8080, debug=True)