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

# Show all the results in the database
@route('/<usrtime:int>/<usrcost:int>/<usrpriority:int>', method='GET')
def show_chimney(usrtime, usrcost, usrpriority):
	db = sqlite3.connect('tasks.db')
	c = db.cursor()
	# c.execute("SELECT * FROM t WHERE (Time < ?)", (usrtime))
	c.execute("SELECT * FROM t WHERE Time <= ? AND Cost <= ? AND Priority <= ?", (usrtime, usrcost, usrpriority,))
	data = c.fetchall()
	c.close()
	output = template('bring_to_picnic', rows=data)
	return output

if __name__ == "__main__": 
	app = bottle.Bottle()
	plugin = bottle.ext.sqlite.Plugin(dbfile='tasks.db')
	app.install(plugin)
	run(host='localhost', port=8081, debug=True)