import os
import json
from flask import Flask, request, jsonify
from simple_websocket import Server, ConnectionClosed

app = Flask(__name__)

connected_users = {}

@app.route("/")
def home():
    return "VoxyzH Server Running!"

@app.route("/ws", websocket=True)
def websocket():
    ws = Server.accept(request.environ)
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
    except ConnectionClosed:
        if user_id and user_id in connected_users:
            del connected_users[user_id]
    return ""

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
