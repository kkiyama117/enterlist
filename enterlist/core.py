from utils import post_message_to_channel
from spread.get_data import GetDataManager
from spread.models import Enter


def run(event: dict):
    # get data from event
    message = event.get("event").get("text")
    commander_id = event.get("event").get("user")
    # send start message
    post_message_to_channel(event.get('event').get('channel'), message + 'command start')
    command, args = parse_command(slack_id=commander_id, message=message)
    if command is not None:
        # gspread からデータを作る
        gspread_manager = GetDataManager()
        enter_data = getattr(gspread_manager, command)(**args)
        res = format_enter(enter_data)
    else:
        res = "No command found!"
    # Slackにメッセージを投稿する
    status = post_message_to_channel(commander_id, res)
    return status


def format_enter(enter):
    text = ""
    if type(enter) is Enter:
        text = enter.detail()
        text = 'エンターをチェックしました\n' + text
    elif type(enter) is list:
        text = ""
        for _enter in enter:
            text += _enter.detail()
        text = f'{len(enter)}人分のエンターをチェックしました\n' + text
    return text


def parse_command(message: str, slack_id: str):
    """Slack message 解析"""
    commands = message.split()
    main_command = commands[0]
    args = None
    if main_command == 'check':
        main_command = 'get'
        args = {'row': int(commands[1])}
    elif main_command == 'check_all':
        main_command = 'get_all'
        args = {'slack_id': slack_id}
    else:
        main_command = None
    return main_command, args
