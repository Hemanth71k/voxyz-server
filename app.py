import os
from flask import Flask, request, jsonify
from flask_sock import Sock
import json

app = Flask(__name__)
sock = Sock(app)

# Store connected users
connected_users = {}

@app.route("/", methods=["GET"])
def home():
    return "VoxyzH Server Running!"

@app.route("/call", methods=["POST"])
def make_call():
    to_number = request.json.get("to")
    message = request.json.get("message")
    return jsonify({"status": "calling"})

@sock.route("/ws")
def websocket(ws):
    user_id = None
    try:
        while True:
            data = ws.receive()
            if data:
                msg = json.loads(data)
                action = msg.get("action")

                if action == "register":
                    user_id = msg.get("user_id")
                    connected_users[user_id] = ws
                    ws.send(json.dumps({"status": "registered"}))

                elif action == "call":
                    target_id = msg.get("target_id")
                    if target_id in connected_users:
                        connected_users[target_id].send(json.dumps({
                            "action": "incoming_call",
                            "from": user_id,
                            "message": msg.get("message")
                        }))

    except:
        if user_id and user_id in connected_users:
            del connected_users[user_id]

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
