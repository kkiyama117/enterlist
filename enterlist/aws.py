# -*- coding: utf-8 -*-
import json
import logging

import boto3

from api import request

# ログ設定
from slack import post_message_to_channel

logger = logging.getLogger()
logger.setLevel(logging.INFO)
# client for call lambda
lambda_client = boto3.client('lambda')


def sender_handler(event, context):
    # 処理
    post_message_to_channel(event.get('event').get('channel'), 'Calling Success!')
    # Slackにメッセージを投稿する
    do_event(event)
    return "OK"


def caller_handler(event: dict, context) -> str:
    # 受け取ったイベント情報をCloud Watchログに出力
    logging.info(json.dumps(event))

    # Event API 認証
    if "challenge" in event:
        return event.get("challenge")

    # ボットによるイベントまたはメッセージ投稿イベント以外の場合
    # 反応させないためにそのままリターンする
    if is_bot(event) or not is_message(event):
        return "OK"

    post_message_to_channel(event.get('event').get('channel'), 'Running...')
    # 非同期処理のため,別関数呼び出し
    lambda_client.invoke(
        FunctionName="enterlist_sender",
        InvocationType="Event",
        Payload=json.dumps(event)
    )
    return "OK"


def is_bot(event: dict) -> bool:
    """ Check Bot or not
    """
    return event.get("event").get("bot_id") is not None


def is_message(event: dict) -> bool:
    """Check Event is created by message send or not"""
    return event.get("event").get("type") == "message"


def do_event(event: dict):
    message = event.get("event").get("text")
    commander_id = event.get("event").get("user")
    post_message_to_channel(event.get('event').get('channel'), message + ' ' + commander_id + ' Searching')
    # gspread からデータを作る
    user_id, res = request(slack_id=commander_id, message=message)
    # Slackにメッセージを投稿する
    status = post_message_to_channel(user_id, res)
    return status


if __name__ == '__main__':
    _id, res = request("U4L4PPWAK", "check 4")
    print(post_message_to_channel(_id, res))
