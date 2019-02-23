# -*- coding: utf-8 -*-
import concurrent.futures
import os
import json
import logging

import requests
from api import request

# ログ設定
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event: dict, context) -> str:
    # 受け取ったイベント情報をCloud Watchログに出力
    logging.info(json.dumps(event))

    # Event API 認証
    if "challenge" in event:
        return event.get("challenge")

    # ボットによるイベントまたはメッセージ投稿イベント以外の場合
    # 反応させないためにそのままリターンする
    if is_bot(event) or not is_message(event):
        return "not apply"

    # 処理
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        # Slackにメッセージを投稿する
        executor.submit(post_message_to_channel, event.get('event').get('channel'), 'Running...')
        executor.submit(do_event, event)
    return "fin"


def is_bot(event: dict) -> bool:
    """ Check Bot or not
    """
    return event.get("event").get("bot_id") is not None


def is_message(event: dict) -> bool:
    """Check Event is created by message send or not"""
    return event.get("event").get("type") == "message"


def do_event(event: dict):
    # gspread からデータを作る
    res = create_response(event)
    # Slackにメッセージを投稿する
    status = post_message_to_channel(event.get("event").get("channel"), res)
    return status


def create_response(event: dict):
    message = event.get("event").get("text")
    user_id = event.get("event").get("user")
    return request(slack_id=user_id, message=message)


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
    logging.info(r)
    return "OK"


if __name__ == '__main__':
    print(post_message_to_channel("@kkiyama117", request("U4L4PPWAK", "console")))
