from urllib import request
from flask import Flask, request, json

app = Flask(__name__)

@app.route("/bot/callback", methods=["POST", "GET" ])
def bot_callback():
    print("request is {}".format(request))
    data = request.json
    print("data is {}".format(data))
    if 'challenge' in data:
        return json.dumps({
            "challenge": request.json['challenge']
    })

    print(data['event']['sender']['sender_id']['open_id'])
    user_open_id = data['event']['sender']['sender_id']['open_id']
    default_respond = json.dumps({
        "success": "cool"
    })
    return default_respond