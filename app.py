#API Flask

from flask import Flask, request, jsonify
from db import get_db
from monitor import check_url
import os

app = Flask(__name__)

API_KEY = os.getenv("API_KEY")

def auth():
    key = request.headers.get("X-API-Key")
    if key != API_KEY:
        return False
    return True

@app.route("/targets", methods=["POST"])
def create_target():
    if not auth():
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    name = data["name"]
    url = data["url"]

    db = get_db()
    cur = db.cursor()
    cur.execute("INSERT INTO targets (name, url) VALUES (%s, %s)", (name, url))
    db.commit()

    return jsonify({"message": "Target created"})


@app.route("/check/<int:target_id>")
def check_target(target_id):
    if not auth():
        return jsonify({"error": "Unauthorized"}), 401

    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM targets WHERE id = %s", (target_id,))
    target = cur.fetchone()

    if not target:
        return jsonify({"error": "Not found"}), 404

    result = check_url(target["url"])

    cur.execute(
        "INSERT INTO metrics (target_id, status, response_time) VALUES (%s, %s, %s)",
        (target_id, result["status"], result["response_time"])
    )
    db.commit()

    return jsonify(result)


@app.route("/metrics/<int:target_id>")
def get_metrics(target_id):
    if not auth():
        return jsonify({"error": "Unauthorized"}), 401

    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute(
        "SELECT * FROM metrics WHERE target_id = %s ORDER BY id DESC LIMIT 20",
        (target_id,)
    )
    return jsonify(cur.fetchall())


if __name__ == "__main__":
    app.run()