from flask import Flask,render_template, Response, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors


app = Flask(__name__)

app.secret_key = 'key'


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'advance'

mysql = MySQL(app)

# @app.route('/')
# def home():
#     return render_template('index.html')

@app.route('/')
def index():
    return render_template('index.html')

 

@app.route('/log', methods=['GET', 'POST'])
def log():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = % s AND password = % s', (username, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            # session['Id'] = account['id']
            # session['Username'] = account['username']
            msg = 'Logged in successfully !'
            return render_template('index.html', msg = 'username')
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)

@app.route("/login/base")
def loggedin():
    if 'loggedin' in session:
        return render_template('base.html', username=session['username'])
    return redirect(url_for('/log'))

@app.route("/logout")
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('email', None)

    return redirect(url_for('home'))

if __name__ == '__main__':
 app.run(debug=True)