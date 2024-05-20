from flask import Flask, render_template, redirect, request, url_for, session, send_file
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import os
from datetime import datetime
from werkzeug.utils import secure_filename






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

@app.route('/courses', methods=['GET', 'POST'])
def courses():
    if request.method == 'POST':
        return redirect(url_for('courses'))
    return render_template('courses.html')

@app.route('/result', methods=['GET', 'POST'])
def result():
    if request.method == 'POST':
        return redirect(url_for('result'))
    return render_template('result.html')


# @app.route('/upload_avatar', methods=['POST'])
# def upload_avatar():
#     avatar = request.files['avatar']
#     filename = secure_filename(avatar.filename)
#     avatar.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#     cursor.execute("UPDATE users SET avatar = %s WHERE id = %s", (, (link unavailable)))
#     mysql.connection.commit()
#     return 'Avatar uploaded successfully!'


# @app.route('/images/<string:filename>')
# def display_image(filename):
#     return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), mimetype='image/jpeg')




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


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM admin WHERE username = % s AND password = % s', (username, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['Id'] = account['id']
            session['Username'] = account['Username']
            msg = 'Logged in successfully !'
            return render_template('admin_dashboard.html', msg = 'username')
        else:
            msg = 'Incorrect username / password !'
    return render_template('admin_login.html', msg = msg)




@app.route('/teacher/login', methods=['GET', 'POST'])
def teacher_login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM teacher WHERE username = % s AND password = % s', (username, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['Id'] = account['id']
            session['Username'] = account['Username']
            msg = 'Logged in successfully !'
            return render_template('teacher.html', msg = 'username')
        else:
            msg = 'Incorrect username / password !'
    return render_template('teacher_login.html', msg = msg)






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
            session['Username'] = account['username']
            msg = 'Logged in successfully !'
            return render_template('user_dashboard.html', msg = 'username')
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)


@app.route('/user_dashboard')
def user_dashboard ():
    return render_template('user_dashboard.html')

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

@app.route("/logout")
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('email', None)

    return redirect(url_for('home'))



@app.route('/')
@app.route('/admin')
def admin():
    cur = mysql.connection.cursor()
    cur.execute("SELECT Fname, Sname, Phone FROM admin")
    data = cur.fetchall()
    cur.execute("SELECT COUNT(*) FROM admin")
    admin_count = cur.fetchone()[0]
    cur.close()
    return render_template('admin.html', data=data, admin_count=admin_count)

@app.route('/teacher')
def teacher():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  Fname, Sname, Phone FROM teacher")
    data = cur.fetchall()
    cur.execute("SELECT COUNT(*) FROM teacher") 
    teacher_count = cur.fetchone()[0]
    cur.close()
    return render_template('teacher.html', data=data, teacher_count=teacher_count)

@app.route('/student')
def student():
    cur = mysql.connection.cursor()
    cur.execute("SELECT Fname, Lname, Adminno FROM student")
    data = cur.fetchall()
    cur.execute("SELECT COUNT(*) FROM student")
    student_count = cur.fetchone()[0]
    cur.close()
    return render_template('student.html', data=data, student_count=student_count)


@app.route('/view/<int:id>')
def view(id):
    return f'Viewing row  with ID {id}'

@app.route('/modify/<int:id>')
def modify(id):
    return f'Modifying row  with ID {id}'

@app.route('/upload', methods=['POST'])
def upload_file():
    cursor = mysql.connection.cursor()
    file = request.files['file']
    cursor.execute('INSERT INTO files (name, data) VALUES(%s, %s)',(file.filename, file.read()))
    mysql.connection.commit()
    return '<h1>File Uploaded Successfully</h1>'








if __name__ == '__main__':
    
    app.run(debug=True)