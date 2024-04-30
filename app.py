from flask import Flask, render_template, redirect, request, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from datetime import datetime





app = Flask(__name__)

app.secret_key = 'key'


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'portal'


mysql = MySQL(app)

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        return redirect(url_for('home'))
    return render_template('index.html')

@app.route('/about', methods=['GET', 'POST'])
def about():
    if request.method == 'POST':
        return redirect(url_for('about'))
    return render_template('about.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')
     
 
@app.route('/register/admin', methods=['GET', 'POST'])
def admin_register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO reg VALUES (NULL, %s, %s, %s)', (username, password, email))
        mysql.connection.commit()
        msg = 'You have successfully registered!'
        return render_template('login.html', msg=msg)
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('admin_register.html', msg=msg)


@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM reg WHERE username = % s AND password = % s', (username, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['Id'] = account['id']
            session['Username'] = account['Username']
            msg = 'Logged in successfully !'
            return render_template('contact.html', msg = 'username')
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)



@app.route('/register/user', methods=['GET', 'POST'])
def user_register():
    msg = ''
    if request.method == 'POST' and 'student' in request.form and 'parent' in request.form and 'former' in request.form and 'address' in request.form :
        student = request.form['student']
        parent = request.form['parent']
        former = request.form['former']
        address = request.form['address']
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO enrol VALUES (NULL, %s, %s, %s, %s, %s)', (student, parent, former, address, datetime.now()))
        mysql.connection.commit()
        msg = 'You have successfully registered!'
        return render_template('login.html', msg=msg)
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('user_register.html', msg=msg)

if __name__ == '__main__':
    
    app.run(debug=True)