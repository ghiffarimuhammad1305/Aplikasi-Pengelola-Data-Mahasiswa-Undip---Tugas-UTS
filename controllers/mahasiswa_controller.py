# controllers/mahasiswa_controller.py - C pada MVC: menerima request, memvalidasi, memutuskan, merespons
from flask import (
    Blueprint,
    abort,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)

from models import mahasiswa_model as model

mahasiswa_bp = Blueprint("mahasiswa_bp", __name__)


def validasi_form(form, nim_diinput=True):
    """Membaca & memeriksa isian form. Mengembalikan (data, daftar_error).
    Backend tidak pernah percaya begitu saja pada kiriman client."""
    errors = []
    data = {}

    # NIM
    if nim_diinput:
        nim_raw = (form.get("nim") or "").strip()
        if not nim_raw:
            errors.append("NIM wajib diisi.")
        elif not nim_raw.isdigit():
            errors.append("NIM harus berupa angka.")
        else:
            data["nim"] = int(nim_raw)

    # Nama & program studi
    data["nama"] = (form.get("nama") or "").strip()
    data["program_studi"] = (form.get("program_studi") or "").strip()
    if not data["nama"]:
        errors.append("Nama wajib diisi.")
    if not data["program_studi"]:
        errors.append("Program studi wajib diisi.")

    # Angkatan
    angkatan_raw = (form.get("angkatan") or "").strip()
    if not angkatan_raw:
        errors.append("Angkatan wajib diisi.")
    elif not angkatan_raw.isdigit() or not (1900 <= int(angkatan_raw) <= 2100):
        errors.append("Angkatan harus berupa tahun yang valid, contoh: 2024.")
    else:
        data["angkatan"] = int(angkatan_raw)

    # IPK
    ipk_raw = (form.get("ipk") or "").strip().replace(",", ".")
    if not ipk_raw:
        errors.append("IPK wajib diisi.")
    else:
        try:
            ipk = float(ipk_raw)
            if not (0.0 <= ipk <= 4.0):
                errors.append("IPK harus berada di rentang 0.00 sampai 4.00.")
            else:
                data["ipk"] = round(ipk, 2)
        except ValueError:
            errors.append("IPK harus berupa angka, contoh: 3.75.")

    return data, errors


# READ (daftar) + dashboard -> GET /
@mahasiswa_bp.route("/", methods=["GET"])
def index():
    keyword = (request.args.get("q") or "").strip()
    return render_template(
        "index.html",
        daftar=model.get_all(keyword or None),
        stats=model.get_stats(),
        keyword=keyword,
    )


# CREATE -> GET (tampilkan form) dan POST (proses form) /mahasiswa/tambah
@mahasiswa_bp.route("/mahasiswa/tambah", methods=["GET", "POST"])
def tambah():
    if request.method == "POST":
        data, errors = validasi_form(request.form)
        if not errors and model.nim_exists(data["nim"]):
            errors.append(f"NIM {data['nim']} sudah terdaftar.")
        if errors:
            for e in errors:
                flash(e, "error")
            return render_template("form.html", mode="tambah", mhs=request.form), 400
        model.create(**data)
        flash(f"Mahasiswa {data['nama']} berhasil ditambahkan.", "success")
        return redirect(url_for("mahasiswa_bp.index"))
    return render_template("form.html", mode="tambah", mhs={})


# READ (detail) -> GET /mahasiswa/<nim>
@mahasiswa_bp.route("/mahasiswa/<int:nim>", methods=["GET"])
def detail(nim):
    mhs = model.get_by_nim(nim)
    if not mhs:
        abort(404)
    return render_template("detail.html", mhs=mhs)


# UPDATE -> GET dan POST /mahasiswa/<nim>/edit
@mahasiswa_bp.route("/mahasiswa/<int:nim>/edit", methods=["GET", "POST"])
def edit(nim):
    mhs = model.get_by_nim(nim)
    if not mhs:
        abort(404)
    if request.method == "POST":
        data, errors = validasi_form(request.form, nim_diinput=False)
        if errors:
            for e in errors:
                flash(e, "error")
            tampil = request.form.to_dict()
            tampil["nim"] = nim
            return render_template("form.html", mode="edit", mhs=tampil), 400
        model.update(nim, **data)
        flash(f"Data {data['nama']} berhasil diperbarui.", "success")
        return redirect(url_for("mahasiswa_bp.index"))
    return render_template("form.html", mode="edit", mhs=mhs)


# DELETE -> POST /mahasiswa/<nim>/hapus
@mahasiswa_bp.route("/mahasiswa/<int:nim>/hapus", methods=["POST"])
def hapus(nim):
    mhs = model.get_by_nim(nim)
    if not mhs:
        abort(404)
    model.delete(nim)
    flash(f"Data {mhs['nama']} berhasil dihapus.", "success")
    return redirect(url_for("mahasiswa_bp.index"))


# Bonus REST API -> GET /api/mahasiswa (JSON)
@mahasiswa_bp.route("/api/mahasiswa", methods=["GET"])
def api_list():
    return jsonify(model.get_all()), 200


@mahasiswa_bp.route("/api/mahasiswa/<int:nim>", methods=["GET"])
def api_detail(nim):
    mhs = model.get_by_nim(nim)
    if not mhs:
        return jsonify({"error": "Mahasiswa tidak ditemukan"}), 404
    return jsonify(mhs), 200


@mahasiswa_bp.app_errorhandler(404)
def not_found(_e):
    return render_template("404.html"), 404
