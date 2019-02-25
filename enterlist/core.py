from api import request
from slack import post_message_to_channel


def do_event(event: dict):
    message = event.get("event").get("text")
    commander_id = event.get("event").get("user")
    post_message_to_channel(event.get('event').get('channel'), message + ' ' + commander_id + ' Searching')
    # gspread からデータを作る
    user_id, res = request(slack_id=commander_id, message=message)
    # Slackにメッセージを投稿する
    status = post_message_to_channel(user_id, res)
    return status