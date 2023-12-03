#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors

#Initialize the app from Flask
app = Flask(__name__)

#Configure MySQL
conn = pymysql.connect(host='localhost',
                       user='root',
                       password='',
                       db='finance',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

#Define a route to hello function
@app.route('/')
def hello():
	return render_template('index.html')

@app.route('/Dashboard', methods=['GET', 'POST'])
def Dashboard():
	# get all the attributes of the logged in user
	cursor = conn.cursor()
	query = 'SELECT * FROM user WHERE username = %s'
	cursor.execute(query, (session['username']))
	data = cursor.fetchall()[0] # NEED THE [0]
	cursor.close()
	error = None

	if(data):
		#creates a session for the the user
		#session is a built in
		return render_template('Dashboard.html', user = data['username'], balance=data['balance'])

@app.route('/register', methods=['GET', 'POST'])
def register():
	return render_template('register.html')

#Authenticates the register
@app.route('/registerAuth', methods=['GET', 'POST'])
def registerAuth():
	#grabs information from the forms
	username = request.form['username']
	password = request.form['password']
	card_number = request.form['card_number']
	balance = request.form['balance']
	# session['balance'] = balance
	cvv = request.form['cvv']
	exp_date = request.form['exp_date']
	credit_score = request.form['credit_score']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM user WHERE username = %s'
	cursor.execute(query, (username))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	error = None
	if(data):
		#If the previous query returns data, then user exists
		error = "This user already exists"
		return render_template('index.html', error = error)
	else:
		ins = 'INSERT INTO user VALUES(%s, %s, %s, %s, %s, %s, %s)'
		cursor.execute(ins, (username, password, balance, card_number, cvv, exp_date, credit_score))
		conn.commit()
		cursor.close()
		return render_template('index.html')

#Authenticates the login
@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
	#grabs information from the forms
	username = request.form['username']
	password = request.form['password']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM user WHERE username = %s and password = %s'
	cursor.execute(query, (username, password))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	error = None
	if(data):
		#creates a session for the the user
		#session is a built in
		session['username'] = username
		return redirect(url_for('Dashboard'))
	else:
		#returns an error message to the html page
		error = 'Invalid login or username'
		return render_template('index.html', error=error)
	
app.secret_key = 'some key that you will never guess'

if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)
