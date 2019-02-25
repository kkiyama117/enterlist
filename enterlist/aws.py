# -*- coding: utf-8 -*-
import json
import logging

import boto3

# ログ設定
from core import run
from utils import post_message_to_channel

logger = logging.getLogger()
logger.setLevel(logging.INFO)
# client for call lambda
lambda_client = boto3.client('lambda')


def sender_handler(event, context):
    """ AWS Sender command

    Args:
        event:
        context:

    Returns:

    """
    # 受け取ったイベント情報をCloud Watchログに出力
    logging.info(json.dumps(event))
    # 処理
    post_message_to_channel(event.get('event').get('channel'), 'Calling Success!')
    # Slackにメッセージを投稿する
    run(event)
    return "OK"


def caller_handler(event: dict, context) -> str:
    """ AWS Sender command

    Args:
        event:
        context:

    Returns:
    """
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
    # 非同期処理のため,別関数(Sender)呼び出し
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
