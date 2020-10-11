from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
#app.config['MYSQL_PASSWORD'] = 'localhost'
app.config['MYSQL_DB'] = 'flaskcontacts'
mysql = MySQL(app)

# Settings
app.secret_key = 'mysecretkey'

@app.route('/')
def index():
    # Consulta a la base de datos
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts')
    data = cur.fetchall()
    return render_template('index.html', contactos = data)

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO contacts (fullname, phone, email) VALUES (%s, %s, %s)', 
        (fullname, phone, email))
        mysql.connection.commit()
        flash('Contacted saved succesfully')
        print(fullname)
        print(phone)
        print(email)
        return redirect(url_for('index'))

@app.route('/edit/<id>', methods = ['POST', 'GET'])
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts WHERE id = %s', [id])
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit_contact.html', contact = data[0])

@app.route('/update/<id>', methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE contacts
            SET fullname = %s,
                email = %s,
                phone = %s
            WHERE id = %s
            """, (fullname, email, phone, id))
        mysql.connection.commit()
        flash('Contact updated succesfully')
        return redirect(url_for('index'))


@app.route('/delete/<string:id>')
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contacts WHERE id={0}'.format(id))
    mysql.connection.commit()
    flash('Contact deleted succesfully')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(port = 3000, debug = True)