from flask import Flask, render_template, request, flash, url_for, redirect
from mysql import connector

app = Flask(__name__)
app.secret_key = 'frankmakanayam'  

db = connector.connect (
    host = 'localhost',
    user = 'root',
    passwd = '',
    database = 'db_kelompok2'
)

if db.is_connected():
    print("berhasil terhubung ke database")

@app.route("/")
def home():
    cursor = db.cursor()
    query = "SELECT nama FROM tbl_anggota"
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
        query = "UPDATE tbl_anggota SET nama = %s WHERE no = %s"
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