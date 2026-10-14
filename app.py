# app.py - menyalakan aplikasi dan menyambungkan semua bagian
from flask import Flask

from controllers.mahasiswa_controller import mahasiswa_bp
from models import mahasiswa_model

app = Flask(__name__)
app.secret_key = "ganti-dengan-kunci-rahasia-kamu"  # dipakai untuk pesan flash

# Pastikan tabel database ada sebelum aplikasi menerima request
mahasiswa_model.init_db()

# Daftarkan controller agar rute-rutenya aktif
app.register_blueprint(mahasiswa_bp)

if __name__ == "__main__":
    app.run(debug=True)
