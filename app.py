from urllib import request
from flask import Flask, request, json

from assistant import *
from utils import *

app = Flask(__name__)

ASSISTANT_BOT_OPEN_ID = "ou_376caaa69595a9fa72425363c34dfc91"

assistant_poll = {}
message_map = {}
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
    message_id = request.json['event']['message']['message_id']
    if message_id in message_map:
        print("message already handled")
        return default_respond
    print(f"deal with message id {message_id}")
    message_map[message_id] = True
    user_msg = get_msg(request.json['event'])
    user_msg_with_open_id = replace_user_with_id(request.json['event'], user_msg)
    assistant = None
    print(f"user_msg_with_open_id {user_msg_with_open_id}")
    if user_open_id not in assistant_poll:
        assistant = Assistant()
        assistant_poll[user_open_id] = assistant
    else:
        assistant = assistant_poll[user_open_id]

    assistant.add_user_message_to_thread(user_msg_with_open_id)

    run = assistant.get_run()
    if run is None:
        print("run is None. ")
        return default_respond

    assistant.execute_run(run)

    response = assistant.get_latest_assistant_message()

    print(response)

    reply_to_user(message_id, response)

    print("reply to user success")
    return default_respond


