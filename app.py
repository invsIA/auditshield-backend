from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
import json
import os

app = Flask(__name__)
CORS(app)

USER_DATA_FILE = 'users.json'

def load_users():
    if not os.path.exists(USER_DATA_FILE):
        return {}
    with open(USER_DATA_FILE, 'r') as f:
        return json.load(f)

def save_users(data):
    with open(USER_DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

@app.route("/start", methods=["POST"])
def start_trial():
    data = request.get_json()
    email = data.get("email", "").strip().lower()
    if not email or "@" not in email:
        return jsonify({"allowed": False, "message": "Invalid email."}), 400

    users = load_users()
    today = datetime.utcnow().date()

    user = users.get(email, {
        "start_date": str(today),
        "attempts_left": 5
    })

    start_date = datetime.strptime(user["start_date"], "%Y-%m-%d").date()
    days_elapsed = (today - start_date).days

    if days_elapsed > 15:
        return jsonify({"allowed": False, "message": "Trial expired. Please upgrade to continue."})

    if user["attempts_left"] <= 0:
        return jsonify({"allowed": False, "message": "You’ve used all 5 free reports. Upgrade to unlock unlimited access."})

    user["attempts_left"] -= 1
    users[email] = user
    save_users(users)

    return jsonify({
        "allowed": True,
        "message": f"You have {user['attempts_left']} free reports left. Enjoy your audit!"
    })

@app.route("/")
def home():
    return jsonify({"message": "AuditShield AI backend is running"})

if __name__ == "__main__":
    app.run(debug=True)