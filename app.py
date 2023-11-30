import json
from urllib import request

from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/bot/callback", methods=["POST"])
def bot_callback():
    print(request)
    if 'challenge' in request.json:
        return json.dumps({
            "challenge": request.json['challenge']
    })

    print(request.json)
    print(request.json['event']['sender']['sender_id']['open_id'])
    user_open_id = request.json['event']['sender']['sender_id']['open_id']
    default_respond = json.dumps({
        "success": "cool"
    })