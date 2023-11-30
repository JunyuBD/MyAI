import json


def bot_mentioned_in_group(event, bot_open_id):
    print(f"message {event['message']}")
    print(f"bot open id: {bot_open_id}")
    if 'mentions' not in event['message']:
        return False

    if bot_open_id != event['message']['mentions'][0]['id']['open_id']:
        return False

    return True


def get_msg(event):
    content = json.loads(event['message']['content'])

    if event['message']['chat_type'] == 'p2p':
        return content['text']

    if event['message']['chat_type'] == 'group':
        raw_msg = content['text']
        valid_msg_list = raw_msg.split(" ")[1:]
        return ' '.join(valid_msg_list)

    print("can not parse user msg")
    return "can not parse user msg"

def replace_user_with_id(event, msg):
    if 'mentions' not in event['message']:
        return msg

    mentions = event['message']['mentions']
    print(f"mentions {mentions}")

    mentions_dict = {}
    for mention in mentions:
        mentions_dict[mention['key']] = f"user_id:{mention['id']['user_id']}"
    print(f"mentions_dict {mentions_dict}")

    msg_list = msg.split(" ")
    for i in range(len(msg_list)):
        if msg_list[i] in mentions_dict:
            msg_list[i] = mentions_dict[msg_list[i]]

    handled_msg = ' '.join(msg_list)
    print(handled_msg)
    return handled_msg