from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import MySQLdb.cursors
from Crypto.Cipher import AES
from base64 import b64encode, b64decode
from Crypto import Random

app = Flask(__name__)

app.secret_key = 'your secret key'

app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '********'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_DB'] = 'form_auth'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

private_key = Random.get_random_bytes(16)
iv = Random.get_random_bytes(16)
cipher = AES.new(private_key, AES.MODE_CFB, iv=iv)

@app.route('/')
@app.route('/insert', methods =['GET', 'POST'])
def insert():
    if request.method == 'POST':
        cipher = AES.new(private_key, AES.MODE_CFB, iv=iv)
        username = b64encode(cipher.encrypt(request.form['username'].encode()))
        email =  b64encode(cipher.encrypt(request.form['email'].encode()))
        age =  b64encode(cipher.encrypt(request.form['age'].encode()))
        address =  b64encode(cipher.encrypt(request.form['address'].encode()))
        pincode =  b64encode(cipher.encrypt(request.form['pincode'].encode()))

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO auth VALUES (%s, %s, %s, %s, %s, %s)', (None, username, email, age, address, pincode,))
        mysql.connection.commit()

        return redirect(url_for('insert'))

    return render_template('insert.html')

@app.route('/view')
def view():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM auth')
    account = cursor.fetchall()
    for x in account:
        cipher = AES.new(private_key, AES.MODE_CFB, iv=iv)
        x['username'] = cipher.decrypt(b64decode(x['username'])).decode()
        x['email'] = cipher.decrypt(b64decode(x['email'])).decode()
        x['age'] = cipher.decrypt(b64decode(x['age'])).decode()
        x['address'] = cipher.decrypt(b64decode(x['address'])).decode()
        x['pincode'] = cipher.decrypt(b64decode(x['pincode'])).decode()

    return render_template('view.html',account=account)

@app.route('/modify/<int:SN>', methods =['GET', 'POST'])
def modify(SN):
    if request.method == 'POST':
        cipher = AES.new(private_key, AES.MODE_CFB, iv=iv)
        username = b64encode(cipher.encrypt(request.form['username'].encode()))
        email =  b64encode(cipher.encrypt(request.form['email'].encode()))
        age =  b64encode(cipher.encrypt(request.form['age'].encode()))
        address =  b64encode(cipher.encrypt(request.form['address'].encode()))
        pincode =  b64encode(cipher.encrypt(request.form['pincode'].encode()))

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE auth SET username = %s, email = %s, age = %s, address = %s, pincode = %s WHERE SN = %s', (username, email, age, address, pincode, SN,))
        mysql.connection.commit()
        return redirect(url_for('view'))

    return render_template('modify.html')


if __name__ == '__main__':
	app.run(debug=True)
