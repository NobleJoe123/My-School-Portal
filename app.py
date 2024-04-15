from flask import Flask, render_template, redirect, request, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors




app = Flask(__name__)

app.secret_key = 'key'


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'pluna'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'Portal'


mysql = MySQL(app)

@app.route("/")
def index():
    return render_template('index.html')




# @app.route('/shop', methods=['GET', 'POST'])
# def shop():
#     if request.method == 'POST':
#         return redirect(url_for('shop'))
#     return render_template('shop.html')@app.route('/log', methods=['GET', 'POST'])



@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'Username' in request.form and 'Password' in request.form:
        Username = request.form['Username']
        Password = request.form['Password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM register WHERE Username = % s AND Password = % s', (Username, Password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['Id'] = account['id']
            session['Username'] = account['Username']
            msg = 'Logged in successfully !'
            return render_template('main.html', msg = 'Username')
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)





if __name__ == '__main__':
    app.run(debug=True)