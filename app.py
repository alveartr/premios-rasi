# app.py

import os
import json
from collections import Counter
from flask import Flask, render_template, request, redirect, url_for, session, flash

from config import (
    CATEGORIES,
    CATEGORY_DESCRIPTIONS,
    CANDIDATES,
    USERS,
    ADMIN_USER,
    PRIMARY_BLUE,
    ACCENT_YELLOW,
    WHITE,
    MAX_SUBMISSIONS_PER_USER,
    USERS_FILE,
    VOTES_FILE,
)

app = Flask(__name__)
app.secret_key = "cambia_esto_por_algo_secreto_y_largo"


# =========================
# Helpers de archivos JSON
# =========================

def load_json(path, default):
    if not os.path.exists(path):
        return default
    with open(path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return default


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def init_data_files():
    """
    Inicializa los archivos users.json y votes.json si no existen.
    Crea 20 usuarios normales + 1 admin.
    """
    # Inicializar usuarios.json
    if not os.path.exists(USERS_FILE):
        users_data = {"users": []}
        user_id = 1

        # Usuarios normales
        for u in USERS:
            users_data["users"].append(
                {
                    "id": user_id,
                    "username": u["username"],
                    "password": u["password"],
                    "submissions": 0,
                    "is_admin": False,
                }
            )
            user_id += 1

        # Usuario admin
        users_data["users"].append(
            {
                "id": user_id,
                "username": ADMIN_USER["username"],
                "password": ADMIN_USER["password"],
                "submissions": 0,
                "is_admin": True,
            }
        )

        save_json(USERS_FILE, users_data)

    # Inicializar votes.json
    if not os.path.exists(VOTES_FILE):
        votes_data = {"votes": []}
        save_json(VOTES_FILE, votes_data)


def get_all_users():
    data = load_json(USERS_FILE, {"users": []})
    return data["users"]


def save_all_users(users):
    save_json(USERS_FILE, {"users": users})


def get_all_votes():
    data = load_json(VOTES_FILE, {"votes": []})
    return data["votes"]


def save_all_votes(votes):
    save_json(VOTES_FILE, {"votes": votes})


def get_current_user():
    user_id = session.get("user_id")
    if not user_id:
        return None
    users = get_all_users()
    for u in users:
        if u["id"] == user_id:
            return u
    return None


def compute_vote_counts():
    """
    Devuelve un dict:
    counts[category_index] = Counter({candidate_index: votos})
    """
    votes = get_all_votes()
    counts = {
        cat_idx: Counter() for cat_idx in range(len(CATEGORIES))
    }
    for v in votes:
        cat = v["category_index"]
        cand = v["candidate_index"]
        if 0 <= cat < len(CATEGORIES) and 0 <= cand < len(CANDIDATES):
            counts[cat][cand] += 1
    return counts


# ✅ IMPORTANTE: inicializamos los archivos de datos al cargar el módulo
init_data_files()


# ==========
# Rutas
# ==========

@app.route("/")
def index():
    if "user_id" in session:
        return redirect(url_for("vote"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        users = get_all_users()
        user = next(
            (u for u in users if u["username"] == username and u["password"] == password),
            None,
        )

        if user:
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["is_admin"] = user.get("is_admin", False)
            flash("Inicio de sesión exitoso.", "success")
            return redirect(url_for("vote"))
        else:
            flash("Usuario o contraseña incorrectos.", "error")

    return render_template(
        "login.html",
        primary_blue=PRIMARY_BLUE,
        accent_yellow=ACCENT_YELLOW,
        white=WHITE,
        username=None,
        is_admin=False,
    )


@app.route("/logout")
def logout():
    session.clear()
    flash("Sesión cerrada.", "info")
    return redirect(url_for("login"))


@app.route("/vote", methods=["GET", "POST"])
def vote():
    user = get_current_user()
    if not user:
        flash("Debes iniciar sesión.", "error")
        return redirect(url_for("login"))

    users = get_all_users()
    # refrescar usuario desde lista
    for u in users:
        if u["id"] == user["id"]:
            user = u
            break

    user_id = user["id"]
    submissions = user.get("submissions", 0)

    votes = get_all_votes()

    # Cargar votos actuales del usuario en un dict: {category_index: candidate_index}
    existing_votes = {}
    for v in votes:
        if v["user_id"] == user_id:
            existing_votes[v["category_index"]] = v["candidate_index"]

    if request.method == "POST":
        if submissions >= MAX_SUBMISSIONS_PER_USER:
            flash("Ya has utilizado tu voto y tu cambio. No puedes modificarlo nuevamente.", "error")
            return redirect(url_for("vote"))

        # Validar que todas las categorías tengan selección
        votes_to_save = {}
        for idx in range(len(CATEGORIES)):
            field_name = f"category_{idx}"
            val = request.form.get(field_name)
            if val is None or val == "":
                flash("Debes votar en TODAS las categorías antes de guardar.", "error")
                return redirect(url_for("vote"))
            try:
                candidate_index = int(val)
            except ValueError:
                flash("Ocurrió un error en el formulario. Intenta de nuevo.", "error")
                return redirect(url_for("vote"))

            if candidate_index < 0 or candidate_index >= len(CANDIDATES):
                flash("Candidato inválido en alguna categoría.", "error")
                return redirect(url_for("vote"))

            votes_to_save[idx] = candidate_index

        # Guardar / actualizar votos en memoria
        for cat_idx, cand_idx in votes_to_save.items():
            # Buscar si ya existe un voto para ese user+category
            found = False
            for v in votes:
                if v["user_id"] == user_id and v["category_index"] == cat_idx:
                    v["candidate_index"] = cand_idx
                    found = True
                    break
            if not found:
                votes.append(
                    {
                        "user_id": user_id,
                        "category_index": cat_idx,
                        "candidate_index": cand_idx,
                    }
                )

        # Actualizar submissions del usuario
        for u in users:
            if u["id"] == user_id:
                u["submissions"] = u.get("submissions", 0) + 1
                submissions = u["submissions"]
                break

        save_all_votes(votes)
        save_all_users(users)

        if submissions == 1:
            flash("Voto registrado. Aún podrás cambiarlo UNA vez más.", "success")
        else:
            flash("Tu voto ha sido ACTUALIZADO. Ya no podrás cambiarlo de nuevo.", "success")

        return redirect(url_for("vote"))

    can_still_edit = submissions < MAX_SUBMISSIONS_PER_USER

    category_data = list(enumerate(CATEGORIES))
    candidates_data = list(enumerate(CANDIDATES))

    return render_template(
        "vote.html",
        category_data=category_data,
        candidates_data=candidates_data,
        category_desc=CATEGORY_DESCRIPTIONS,
        existing_votes=existing_votes,
        can_still_edit=can_still_edit,
        submissions=submissions,
        max_submissions=MAX_SUBMISSIONS_PER_USER,
        primary_blue=PRIMARY_BLUE,
        accent_yellow=ACCENT_YELLOW,
        white=WHITE,
        username=session.get("username"),
        is_admin=session.get("is_admin", False),
    )


@app.route("/nominated")
def nominated():
    """
    Vista para TODOS los usuarios: muestra solo los NOMINADOS (top 5 por categoría),
    ordenados alfabéticamente, sin cantidades de votos.
    """
    user = get_current_user()
    if not user:
        flash("Debes iniciar sesión.", "error")
        return redirect(url_for("login"))

    counts = compute_vote_counts()

    # nominated_data[cat_idx] = [lista de nombres nominados]
    nominated_data = {}
    for cat_idx in range(len(CATEGORIES)):
        counter = counts[cat_idx]  # Counter({candidate_index: votos})

        # Lista de (candidate_index, votos) ordenada desc por votos, luego por nombre
        items = sorted(
            counter.items(),
            key=lambda x: (-x[1], CANDIDATES[x[0]].lower())
        )

        top_indices = [cand_idx for cand_idx, _ in items[:5]]
        top_names = [CANDIDATES[i] for i in top_indices]

        # Orden alfabético por nombre
        top_names_sorted = sorted(top_names, key=lambda s: s.lower())

        nominated_data[cat_idx] = top_names_sorted

    category_data = list(enumerate(CATEGORIES))

    return render_template(
        "nominated.html",
        category_data=category_data,
        nominated_data=nominated_data,
        primary_blue=PRIMARY_BLUE,
        accent_yellow=ACCENT_YELLOW,
        white=WHITE,
        username=session.get("username"),
        is_admin=session.get("is_admin", False),
    )


@app.route("/admin/results", methods=["GET", "POST"])
def admin_results():
    """
    Vista solo para ADMIN:
    - Selecciona categoría
    - Ve todos los candidatos con cantidad de votos, ordenados de mayor a menor
    """
    user = get_current_user()
    if not user or not user.get("is_admin", False):
        flash("Acceso solo para administrador.", "error")
        return redirect(url_for("login"))

    selected_category_index = 0
    if request.method == "POST":
        cat_str = request.form.get("category_index", "0")
        try:
            selected_category_index = int(cat_str)
        except ValueError:
            selected_category_index = 0

    if selected_category_index < 0 or selected_category_index >= len(CATEGORIES):
        selected_category_index = 0

    counts = compute_vote_counts()
    counter = counts[selected_category_index]

    # Construimos lista (nombre_candidato, votos) para TODOS los candidatos,
    # incluyendo los que tienen 0 votos
    results_list = []
    for cand_idx, cand_name in enumerate(CANDIDATES):
        votes = counter.get(cand_idx, 0)
        results_list.append((cand_name, votes))

    # Ordenar desc por votos, luego alfabéticamente
    results_list.sort(key=lambda x: (-x[1], x[0].lower()))

    category_data = list(enumerate(CATEGORIES))

    return render_template(
        "admin_results.html",
        category_data=category_data,
        selected_category_index=selected_category_index,
        results_list=results_list,
        primary_blue=PRIMARY_BLUE,
        accent_yellow=ACCENT_YELLOW,
        white=WHITE,
        username=session.get("username"),
        is_admin=True,
    )


if __name__ == "__main__":
    # En Mac o VPS puedes usar esto directamente
    app.run(host="0.0.0.0", port=5001, debug=False)