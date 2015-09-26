from bottle import route, run, template, static_file
import pandas as pd
import os
import csv, sqlite3
import bottle.ext.sqlite


@route('/show/:item')
def show(item, db):
	row = db.execute('SELECT * from items where name=?', item).fetchone()
	if row:
		return template('showitem', page=row)
	return HTTPSError(404, 'Page not found')

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

# Show all the results in the database
@route('/chimney')
def show_chimney():
	db = sqlite3.connect('tasks.db')
	c = db.cursor()
	c.execute("SELECT * FROM t WHERE Time < 8")
	data = c.fetchall()
	c.close()
	output = template('bring_to_picnic', rows=data)
	return output

def filter_data(cost, time, priority):
	data_loc = 'task_data.csv'
	df = pd.read_csv(data_loc)
	print cost
	a = df.query('Cost <= ' + str(cost) + ' & ' + 'Time <= ' + str(time) + ' & ' + 'Priority <= ' + str(priority))
	#return str(a)
	#return "Cost: " + cost + "," + "priority: " + priority
	return a.to_html(classes='my_class')

if __name__ == "__main__": 
	app = bottle.Bottle()
	plugin = bottle.ext.sqlite.Plugin(dbfile='tasks.db')
	app.install(plugin)
	run(host='localhost', port=8080, debug=True)