import os

import requests


def post_message_to_channel(channel: str, message: str):
    """
    Send message to slack
    Args:
        channel: ID of Channnel or member to send message
        message: text of message

    Returns:

    """
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
    requests.post(url, headers=headers, data=payload)
    return "OK"
