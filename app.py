import os
from flask import Flask, request
from twilio.rest import Client

app = Flask(__name__)

ACCOUNT_SID = os.environ.get("ACCOUNT_SID")
AUTH_TOKEN = os.environ.get("AUTH_TOKEN")
TWILIO_NUMBER = os.environ.get("TWILIO_NUMBER")

client = Client(ACCOUNT_SID, AUTH_TOKEN)

@app.route("/call", methods=["POST"])
def make_call():
    to_number = request.json.get("to")
    message = request.json.get("message", "This is a recorded message from VoxyzH")

    call = client.calls.create(
        tts=message,
        to=to_number,
        from_=TWILIO_NUMBER
    )

    return {"status": "calling", "sid": call.sid}

@app.route("/", methods=["GET"])
def home():
    return "VoxyzH Server Running!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port, debug=False)
