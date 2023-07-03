from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL


app = Flask(__name__)
app.config['SECRET_KEY'] = 'skey'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask_example_db'

mysql = MySQL(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/database')
def database():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM students')
    data = cur.fetchall()
    cur.close()
    return render_template('database.html', students=data)

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        city = request.form['city']

        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO students (name, phone, email, city) VALUES (%s, %s, %s, %s)",
            (name, phone, email, city)
        )
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('database'))

    return render_template('add_student.html')

@app.route('/remove_student', methods=['GET', 'POST'])
def remove_student():
    if request.method == 'POST':
        student_id = request.form['student_id']
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM students WHERE id = %s", (student_id,))
        mysql.connection.commit()
        cur.close()
        flash('Studen removed successfully')
        return redirect(url_for('database'))
    else:
        return render_template('remove_student.html')


if __name__ == '__main__':
    app.run(debug=True)
