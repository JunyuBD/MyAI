import random
from urllib import request
from flask import Flask, request, json
import threading
from assistant import *
from utils import *

app = Flask(__name__)

ASSISTANT_BOT_OPEN_ID = "ou_376caaa69595a9fa72425363c34dfc91"

assistant_poll = {}
message_map = {}


# Function to handle time-consuming task
def handle_time_consuming_task(user_open_id, user_message, message_id):
    print("====== starting thread ====== for user {}, message {}, message id {}".format(user_open_id, user_message, message_id))
    if user_open_id not in assistant_poll:
        assistant = Assistant()
        assistant_poll[user_open_id] = assistant
    else:
        assistant = assistant_poll[user_open_id]

    assistant.add_user_message_to_thread(user_message)

    run = assistant.get_run()
    if run is None:
        print("run is None. ")
        return

    assistant.execute_run(run)

    response = assistant.get_latest_assistant_message()

    print(response)

    reply_to_user(message_id, response)

    print("reply to user success")


@app.route("/bot/callback", methods=["POST", "GET" ])
def bot_callback():
    data = request.json
    print("data is {}".format(data))
    if 'challenge' in data:
        return json.dumps({
            "challenge": request.json['challenge']
    })

    sleep_time = random.uniform(0, 3)
    default_respond = json.dumps({
        "success": "cool"
    })
    # Pause the program for the generated duration
    time.sleep(sleep_time)

    message_id = request.json['event']['message']['message_id']
    print(f"Slept for {sleep_time} seconds, for message id {message_id}")
    if message_id in message_map:
        print("message already handled")
        return default_respond

    message_map[message_id] = True

    print(data['event']['sender']['sender_id']['open_id'])
    if data['event']['sender']['sender_id']['open_id'] != "ou_aaa0199b52b1044cd44c043245927932":
        reply_to_user(message_id, "Sorry, the beta is unstable so it only allow certain users to test.")

    user_open_id = data['event']['sender']['sender_id']['open_id']

    has_mention = bot_mentioned_in_group(request.json['event'], ASSISTANT_BOT_OPEN_ID)
    print(f"has mention {has_mention}")

    if not has_mention :
        print('bot not mentioned in the group')
        return default_respond

    if request.json['event']['message']['chat_type'] != 'group' :
        print("not as group")
        return default_respond


    user_msg = get_msg(request.json['event'])
    user_msg_with_open_id = replace_user_with_id(request.json['event'], user_msg)

    print("user msg is {}".format(user_msg_with_open_id))
    assistant = None

    print("====== starting thread ====== for {}".format(user_open_id))
    # thread = threading.Thread(target=handle_time_consuming_task, args=(user_open_id, user_msg_with_open_id, message_id,))
    # thread.start()
    time.sleep(10)
    reply_to_user(message_id, "I am processing your request, please wait a moment. ")
    return default_respond


