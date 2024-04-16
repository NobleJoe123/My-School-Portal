from flask import Flask, render_template, redirect, request, url_for, session
from datetime import datetime
from flask_mysqldb import MySQL
import MySQLdb.cursors




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
     
 
@app.route('/reg', methods=['GET', 'POST'])
def reg():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO reg VALUES (NULL, %s, %s, %s)', (username, password, email,))
        mysql.connection.commit()
        msg = 'You have successfully registered!'
        return render_template('login.html', msg=msg)
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('register.html', msg=msg)


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



@app.route('/enrol', methods=['GET', 'POST'])
def enrol():
    msg = ''
    if request.method == 'POST' and 'studentname' in request.form and 'parentmobile' in request.form and 'formerclass' in request.form and 'address' in request.form:
        studentname = request.form['studentname']
        parentmobile = request.form['parentmobile']
        formerclass = request.form['formerclass']
        address = request.form['address']
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO enrol VALUES (NULL, %s, %s, %s, %s)', (studentname, parentmobile,formerclass,address))
        mysql.connection.commit()
        msg = 'You are successfully a student!'
        return render_template('login.html', msg=msg)
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('enrol.html', msg=msg)


if __name__ == '__main__':
    app.run(debug=True)