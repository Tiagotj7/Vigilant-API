# app.py
from flask import Flask, request, jsonify
from db import get_db
from monitor import check_url
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # libera consumo pelo frontend PHP

API_KEY = os.getenv("API_KEY")

def auth():
    key = request.headers.get("X-API-Key")
    return key == API_KEY

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/targets", methods=["POST"])
def create_target():
    if not auth():
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json(silent=True) or {}
    name = data.get("name")
    url = data.get("url")

    if not name or not url:
        return jsonify({"error": "name and url are required"}), 400

    try:
        db = get_db()
        cur = db.cursor()
        cur.execute("INSERT INTO targets (name, url) VALUES (%s, %s)", (name, url))
        db.commit()
        cur.close()
        db.close()
        return jsonify({"message": "Target created"}), 201
    except Exception as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500


@app.route("/check/<int:target_id>")
def check_target(target_id):
    if not auth():
        return jsonify({"error": "Unauthorized"}), 401

    try:
        db = get_db()
        cur = db.cursor(dictionary=True)
        cur.execute("SELECT * FROM targets WHERE id = %s", (target_id,))
        target = cur.fetchone()

        if not target:
            cur.close()
            db.close()
            return jsonify({"error": "Not found"}), 404

        result = check_url(target["url"])

        cur.execute(
            "INSERT INTO metrics (target_id, status, response_time) VALUES (%s, %s, %s)",
            (target_id, result["status"], result["response_time"])
        )
        db.commit()
        cur.close()
        db.close()

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": "Check failed", "details": str(e)}), 500


@app.route("/metrics/<int:target_id>")
def get_metrics(target_id):
    if not auth():
        return jsonify({"error": "Unauthorized"}), 401

    try:
        db = get_db()
        cur = db.cursor(dictionary=True)
        cur.execute(
            "SELECT id, status, response_time, created_at "
            "FROM metrics WHERE target_id = %s ORDER BY id DESC LIMIT 20",
            (target_id,)
        )
        rows = cur.fetchall()
        cur.close()
        db.close()

        return jsonify(rows), 200

    except Exception as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500


if __name__ == "__main__":
    # Apenas para dev local. No Render, quem sobe é o gunicorn.
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
