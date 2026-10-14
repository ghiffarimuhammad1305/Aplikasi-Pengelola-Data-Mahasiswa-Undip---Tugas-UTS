# Aplikasi Data Mahasiswa (UTS Lab Pemrograman 2026/2027)

CRUD data mahasiswa dengan **Python + Flask**, database **SQLite**, pola **MVC**, tampilan dashboard bernuansa Undip.

## Menjalankan di Mac (VS Code)

```bash
cd mahasiswa-app
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

Buka http://127.0.0.1:5000. File database `mahasiswa.db` dibuat otomatis dan datanya tetap ada setelah aplikasi dimatikan.
Data contoh (opsional): `python3 seed_data.py`

## Logo Undip

Simpan logo resmi sebagai `static/img/logo-undip.png` (PNG, latar transparan lebih bagus). Selama file itu belum ada, aplikasi memakai logo sementara `logo-undip-placeholder.svg`.

## Struktur

```
app.py                              menyalakan & menyambungkan semua bagian
models/mahasiswa_model.py           M: akses database SQLite + hitung Lama Studi
controllers/mahasiswa_controller.py C: rute, validasi, keputusan, respons
templates/                          V: tampilan HTML (Jinja)
static/css/style.css                gaya (palet biru tua + emas Undip)
```

## Rute

| Aksi | Method | Alamat |
|---|---|---|
| Dashboard + daftar | GET | `/` (cari: `/?q=kata`) |
| Create | GET, POST | `/mahasiswa/tambah` |
| Read detail | GET | `/mahasiswa/<nim>` |
| Update | GET, POST | `/mahasiswa/<nim>/edit` |
| Delete | POST | `/mahasiswa/<nim>/hapus` |
| JSON (bonus) | GET | `/api/mahasiswa`, `/api/mahasiswa/<nim>` |

## Aturan yang diterapkan

- `nim`, `nama`, `program_studi`, `angkatan`, `ipk` wajib diisi; `ipk` harus 0.00 sampai 4.00, jika tidak ditolak dengan pesan kesalahan.
- NIM yang sudah terdaftar ditolak saat tambah.
- Lama Studi = tahun sekarang - angkatan, dihitung program (`_tambah_lama_studi` di model), tidak diinput pengguna.
