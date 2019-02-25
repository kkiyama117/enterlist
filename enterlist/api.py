from spread.get_data import GetDataManager
from spread.models import format_enter


def request(slack_id: str, message: str) -> (str, str):
    gspread_manager = GetDataManager()
    command, args = parse_command(message=message, slack_id=slack_id)
    if command is not None:
        enter_data = getattr(gspread_manager, command)(**args)
        return slack_id, format_enter(enter_data)
    else:
        return slack_id, "No command found!"


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
