from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'ROOT'
app.config['MYSQL_DB'] = 'ap2b_kursus'
app.config['MYSQL_PORT'] = 3307  # set the port as an integer
mysql = MySQL(app)


@app.route('/')
def users():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM kursus')
    data = cur.fetchall()
    cur.close()
    return render_template('home.html', computers=data)  # use named variable instead of string

@app.route('/simpan', methods=['POST'])
def simpan():
    nama = request.form['nama']
    alamat = request.form['alamat']
    telp = request.form['telp']
    jeniskelamin = request.form['jeniskelamin']
    jeniskursus = request.form['jeniskursus']
    cur = mysql.connection.cursor()
    cur.execute('INSERT INTO kursus (Nama, Alamat, Telp, Jenis_kelamin, Jenis_kursus) VALUES (%s, %s, %s, %s, %s)', (nama, alamat, telp, jeniskelamin, jeniskursus,))
    mysql.connection.commit()
    return redirect(url_for('users'))

@app.route('/update', methods=['POST'])
def update():
    id_data = request.form['id']
    nama = request.form['nama']
    alamat = request.form['alamat']
    telp = request.form['telp']
    jeniskelamin = request.form['jeniskelamin']
    jeniskursus = request.form['jeniskursus']
    cur = mysql.connection.cursor()
    cur.execute('UPDATE kursus SET Nama= %s, Alamat= %s, Telp= %s, Jenis_kelamin= %s, Jenis_kursus= %s WHERE No=%s', (nama ,alamat, telp, jeniskelamin, jeniskursus,id_data,) )
    mysql.connection.commit()
    return redirect(url_for('users'))

@app.route('/hapus/<string:id_data>', methods=['GET'])
def hapus(id_data):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM kursus WHERE No=%s', (id_data) )
    mysql.connection.commit()
    return redirect(url_for('users'))

@app.route('/api/users', methods=['GET'])
def get_users():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM kursus')
    data = cur.fetchall()
    cur.close()
    users = []
    for row in data:
        user = {
            'id': row[0],
            'nama': row[1],
            'alamat': row[2],
            'telp': row[3],
            'jeniskelamin': row[4],
            'jeniskursus': row[5]
        }
        users.append(user)
    return render_template('main.html', users=users)
if __name__ == '__main__':
    app.run(debug=True)