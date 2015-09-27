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
@route('/<usrtime:int>/<usrcost:int>/<usrpriority:int>', method='GET')
def show_chimney(usrtime, usrcost, usrpriority):
	db = sqlite3.connect('tasks.db')
	c = db.cursor()
	c.execute("SELECT * FROM t WHERE Time <= ? AND Cost <= ? AND Priority <= ?", (usrtime, usrcost, usrpriority,))
	data = c.fetchall()
	c.close()
	output = template('bring_to_picnic', rows=data)
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

		return '<p>The new task was inserted; the ID is %s</p>' % new_id
	else:
		return template('new_task.tpl')

# Edit an existing task
@route('/edit/<no:int>', method='GET')
def edit_item(no):

	if request.GET.get('save', '').strip():
		task = request.GET.get('Task', '').strip()
		time = request.GET.get('Time', '').strip()
		cost = request.GET.get('Cost', '').strip()
		priority = request.GET.get('Priority', '').strip()
		status = request.GET.get('Status', '').strip()
		conn = sqlite3.connect('tasks.db')
		c = conn.cursor()
		# c.execute('UPDATE t SET Task = ? WHERE rowid LIKE ?', (task,no))
		c.execute('UPDATE t SET Task=?, Time=?, Cost=?, Priority=?, Status=? WHERE rowid LIKE ?', 
			(task, int(time), int(cost), int(priority), status, no))
		conn.commit()

		return '<p>The item number %s was successfully updated</p>' % no
	else:
		conn = sqlite3.connect('tasks.db')
		c = conn.cursor()
		c.execute('SELECT Task FROM t WHERE rowid LIKE ?', (str(no),))
		cur_data = c.fetchone()

		return template('edit_task', old=cur_data, no=no)

# Remove a task

if __name__ == "__main__": 
	app = bottle.Bottle()
	plugin = bottle.ext.sqlite.Plugin(dbfile='tasks.db')
	app.install(plugin)
	run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)
	#run(host='0.0.0.0', port=8080, debug=False)
