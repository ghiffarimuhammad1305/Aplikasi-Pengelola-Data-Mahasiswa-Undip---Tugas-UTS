# Opsional: isi beberapa data contoh agar dashboard tidak kosong saat demo/video.
# Jalankan:  python3 seed_data.py
from models import mahasiswa_model as model

model.init_db()
contoh = [
    (12010124140001, "Andi Pratama", "Bisnis Digital", 2024, 3.75),
    (12010124140002, "Budi Santoso", "Bisnis Digital", 2023, 3.40),
    (12010123140003, "Citra Lestari", "Manajemen", 2023, 3.90),
    (12010122140004, "Dewi Anggraini", "Akuntansi", 2022, 3.55),
]
for row in contoh:
    if not model.nim_exists(row[0]):
        model.create(*row)
print("Data contoh siap.")
