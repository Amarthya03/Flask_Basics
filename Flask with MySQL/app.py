from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)

# * Configure DB
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index():

	if request.method =='POST':
		userDetails = request.form
		name = userDetails['name']
		email = userDetails['email']
		cursor = mysql.connection.cursor()
		cursor.execute("insert into login(name, email) values(%s, %s)", (name, email))
		mysql.connection.commit()
		cursor.close()
		return redirect('/users')

	return render_template('index.html')

@app.route('/users', methods=['GET', 'POST'])
def users():
	cursor = mysql.connection.cursor()
	resultValue = cursor.execute("select * from login")
	
	if resultValue > 0:
		userDetails = cursor.fetchall()
		return render_template('users.html', userDetails=userDetails)


if __name__ == '__main__':
	app.run(debug=True)