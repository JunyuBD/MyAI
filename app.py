from urllib import request
from flask import Flask, request, json
from utils import *

app = Flask(__name__)

ASSISTANT_BOT_OPEN_ID = "ou_376caaa69595a9fa72425363c34dfc91"

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

    if request.json['event']['message']['chat_type'] == 'group' and not bot_mentioned_in_group(request.json['event'], ASSISTANT_BOT_OPEN_ID):
        print('bot not mentioned in the group')
        return default_respond

    user_msg = get_msg(request.json['event'])
    user_msg_with_open_id = replace_user_with_id(request.json['event'], user_msg)

    print(f"user_msg_with_open_id {user_msg_with_open_id}")

    return default_respond