# models/mahasiswa_model.py - M pada MVC: semua urusan data ada di sini
import os
import sqlite3
from datetime import date

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "mahasiswa.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # hasil query bisa diakses seperti dictionary
    return conn


def init_db():
    """Membuat tabel mahasiswa jika belum ada. Data tetap ada setelah aplikasi dimatikan."""
    conn = get_connection()
    with conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS mahasiswa (
                nim INTEGER PRIMARY KEY,
                nama TEXT NOT NULL,
                program_studi TEXT NOT NULL,
                angkatan INTEGER NOT NULL,
                ipk REAL NOT NULL
            )
            """
        )
    conn.close()


def _tambah_lama_studi(row):
    """Lama Studi dihitung oleh program: tahun sekarang - angkatan."""
    data = dict(row)
    data["lama_studi"] = date.today().year - data["angkatan"]
    return data


def get_all(keyword=None):
    sql = "SELECT * FROM mahasiswa"
    params = []
    if keyword:
        sql += " WHERE nama LIKE ? OR CAST(nim AS TEXT) LIKE ? OR program_studi LIKE ?"
        like = f"%{keyword}%"
        params = [like, like, like]
    sql += " ORDER BY nama COLLATE NOCASE"
    conn = get_connection()
    rows = conn.execute(sql, params).fetchall()
    conn.close()
    return [_tambah_lama_studi(r) for r in rows]


def get_by_nim(nim):
    conn = get_connection()
    row = conn.execute("SELECT * FROM mahasiswa WHERE nim = ?", (nim,)).fetchone()
    conn.close()
    return _tambah_lama_studi(row) if row else None


def nim_exists(nim):
    conn = get_connection()
    row = conn.execute("SELECT 1 FROM mahasiswa WHERE nim = ?", (nim,)).fetchone()
    conn.close()
    return row is not None


def create(nim, nama, program_studi, angkatan, ipk):
    conn = get_connection()
    with conn:
        conn.execute(
            "INSERT INTO mahasiswa (nim, nama, program_studi, angkatan, ipk) VALUES (?, ?, ?, ?, ?)",
            (nim, nama, program_studi, angkatan, ipk),
        )
    conn.close()


def update(nim, nama, program_studi, angkatan, ipk):
    conn = get_connection()
    with conn:
        cur = conn.execute(
            "UPDATE mahasiswa SET nama = ?, program_studi = ?, angkatan = ?, ipk = ? WHERE nim = ?",
            (nama, program_studi, angkatan, ipk, nim),
        )
    changed = cur.rowcount > 0
    conn.close()
    return changed


def delete(nim):
    conn = get_connection()
    with conn:
        cur = conn.execute("DELETE FROM mahasiswa WHERE nim = ?", (nim,))
    changed = cur.rowcount > 0
    conn.close()
    return changed


def get_stats():
    """Ringkasan untuk dashboard."""
    conn = get_connection()
    total, rata, tertinggi, jml_prodi = conn.execute(
        "SELECT COUNT(*), AVG(ipk), MAX(ipk), COUNT(DISTINCT program_studi) FROM mahasiswa"
    ).fetchone()
    per_prodi = conn.execute(
        "SELECT program_studi, COUNT(*) AS jumlah FROM mahasiswa "
        "GROUP BY program_studi ORDER BY jumlah DESC, program_studi"
    ).fetchall()
    conn.close()
    return {
        "total": total,
        "rata_ipk": rata or 0,
        "ipk_tertinggi": tertinggi or 0,
        "jumlah_prodi": jml_prodi,
        "per_prodi": [dict(r) for r in per_prodi],
    }
