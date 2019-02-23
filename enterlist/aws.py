# -*- coding: utf-8 -*-
import os
import json
import logging

import requests

# ログ設定
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event: dict, context) -> str:
    # 受け取ったイベント情報をCloud Watchログに出力
    logging.info(json.dumps(event))

    # Event APIの認証
    if "challenge" in event:
        return event.get("challenge")

    # ボットによるイベントまたはメッセージ投稿イベント以外の場合
    # 反応させないためにそのままリターンする
    if is_bot(event) or not is_message(event):
        return "OK"

    # Slackにメッセージを投稿する
    return post_message_to_channel(event.get("event").get("channel"), "Hello, Slack Bot!")


def is_bot(event: dict) -> bool:
    return event.get("event").get("bot_id") is not None


def is_message(event: dict) -> bool:
    return event.get("event").get("type") == "message"


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
    return "fin"
