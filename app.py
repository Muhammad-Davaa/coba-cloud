from flask import Flask, render_template, request, flash, url_for, redirect

import pypyodbc as odbc 
import pandas as pd

connection_string = 'Driver={ODBC Driver 18 for SQL Server};Server=tcp:kelompok2db.database.windows.net,1433;Database=kelompok2db;Uid=davaramadhana;Pwd=Davamama4;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
db = odbc.connect(connection_string)

app = Flask(__name__)
app.secret_key = 'frankmakanayam'  

@app.route("/")
def home():
    cursor = db.cursor()
    query = "SELECT nama FROM [dbo].[db_kelompok2]"
    cursor.execute(query)
    results = cursor.fetchall()  # Ambil semua baris hasil
    cursor.close()

    # Ambil semua nama dari hasil query
    nama_anggota = [result[0] for result in results] if results else None

    # Kirim hasil ke template HTML
    return render_template('index.html', hasil=nama_anggota)

@app.route("/anggota")
def anggota():
    return render_template('anggota.html')

@app.route("/edit")
def edit():
    return render_template('edit.html')

@app.route('/ubah-nama/<int:id>', methods=['GET', 'POST'])
def ubah_nama(id):
    if request.method == 'POST':
        nama_baru = request.form['nama_baru1']
        
        cursor = db.cursor()
        query = "UPDATE [dbo].[db_kelompok2] SET nama = ? WHERE no = ?"
        cursor.execute(query, (nama_baru, id))
        db.commit()
        cursor.close()

        if request.method == 'POST':
            nama = request.form.get('nama_baru1')
        if not nama:
            flash('Nama tidak boleh kosong', 'error')
        else:
            flash('Data berhasil diubah', 'success')
            # Lakukan operasi penyimpanan data atau operasi lain yang diperlukan
            return redirect(url_for('edit'))

    return render_template('edit.html')


if __name__ == "__main__":
    app.run(debug=True)