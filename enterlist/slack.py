import os

import requests


def post_message_to_channel(channel: str, message: str):
    # load_dotenv(find_dotenv())
    url = "https://slack.com/api/chat.postMessage"
    token = os.getenv('SLACK_BOT_TOKEN')
    headers = {
        "Authorization": "Bearer " + token
    }
    payload = {
        'channel': channel,
        'text': message,
        'as_user': True
    }
    r = requests.post(url, headers=headers, data=payload)
    return "OK"
