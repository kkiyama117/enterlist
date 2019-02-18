import os

import requests
from dotenv.main import find_dotenv, load_dotenv


def test():
    load_dotenv(find_dotenv())
    url = 'https://slack.com/api/chat.postMessage'
    token = os.getenv('SLACK_BOT_TOKEN')
    headers = {"Authorization": "Bearer " + token}
    channel = "@kkiyama117"  # ユーザーを指定するとDMが送られる
    payload = {
        'channel': channel,
        'text': "tset",
        'as_user': True
    }
    r = requests.post(url, headers=headers, data=payload)
    print(r.text)


if __name__ == '__main__':
    test()
