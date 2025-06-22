from flask import Flask, jsonify

app = Flask(_name_)

@app.route("/")
def home():
    return jsonify({"message": "AuditShield AI backend is running"})

if _name_ == "_main_":
    app.run()
