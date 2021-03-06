from bottle import route, run, template, static_file, request
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
@route('/<mintime:int>/<maxtime:int>/<mincost:int>/<maxcost:int>/<usrpriority:int>', method='GET')
def show_chimney(mintime, maxtime, mincost, maxcost, usrpriority):
	db = sqlite3.connect('tasks.db')
	c = db.cursor()
	c.execute("SELECT Task, Time, Cost, Priority, Status, rowid \
	 FROM t WHERE \
	 Time >= ? AND Time <= ? AND \
	 Cost >= ? AND Cost <= ? AND \
	 Priority <= ?", 
		(mintime, maxtime, mincost, maxcost, usrpriority,))
	data = c.fetchall()
	# Fetch the row id of the query

	c.close()
	output = template('task_list', rows=data, query=[mintime, maxtime, mincost, maxcost, usrpriority])
	return output


# Add a new tasks
@route('/new', method='GET')
def new_item():

	if request.GET.get('save', '').strip():
		newTask = request.GET.get('Task', '').strip()
		newTime = request.GET.get('Time', '').strip()
		newCost = request.GET.get('Cost', '').strip()
		newPriority = request.GET.get('Priority', '').strip()
		newStatus = request.GET.get('Status', '').strip()
		conn = sqlite3.connect('tasks.db')
		c = conn.cursor()

		c.execute('INSERT INTO t (Task, Time, Cost, Priority, Status) VALUES (?,?,?,?,?)', (newTask,int(newTime),int(newCost),int(newPriority), newStatus))
		new_id = c.lastrowid

		conn.commit()
		c.close()

		# return '<p>The new task was inserted; the ID is %s</p>' % new_id
		return '<p>item added</p>'
	else:
		return template('new_task.tpl')

# Edit an existing task
@route('/edit/<no:int>', method='GET')
def edit_item(no):
	conn = sqlite3.connect('tasks.db')
	c = conn.cursor()
	if request.GET.get('save', '').strip():
		task = request.GET.get('Task', '').strip()
		time = request.GET.get('Time', '').strip()
		cost = request.GET.get('Cost', '').strip()
		priority = request.GET.get('Priority', '').strip()
		status = request.GET.get('Status', '').strip()
		c.execute('UPDATE t SET Task=?, Time=?, Cost=?, Priority=?, Status=? WHERE rowid LIKE ?', 
			(task, int(time), int(cost), int(priority), status, no))
		conn.commit()

		# return template('test', no=no)
		return '<p>item edited</p>'

	elif request.GET.get('delete', '').strip():
		c.execute('DELETE FROM t WHERE rowid LIKE ?', (no,))
		conn.commit()

		# return template('test', no=no)
		return '<p>item deleted</p>'

	else:
		c.execute('SELECT Task, Time, Cost, Priority, Status FROM t WHERE rowid LIKE ?', (str(no),))
		cur_data = c.fetchone()

		return template('edit_task', old=cur_data, no=no)

if __name__ == "__main__": 
	app = bottle.Bottle()
	plugin = bottle.ext.sqlite.Plugin(dbfile='tasks.db')
	app.install(plugin)
	run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)
	#run(host='0.0.0.0', port=8080, debug=False)
