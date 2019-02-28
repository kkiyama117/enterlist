import core

_commands_dict = {'check': 'confirm_enters_data'}


def request(event: dict):
    # get data from event
    message = event.get("event").get("text")
    commander_id = event.get("event").get("user")
    _command = parse_command(message)
    if _command == "all":
        _commands = _commands_dict.values()
    else:
        _commands = [_command]
    answer = []
    for x in _commands:
        answer.append(getattr(core, x)(user_id=commander_id))
    return answer


def parse_command(message: str):
    """Slack message 解析"""
    commands = message.split()
    main_command = commands[0]
    if main_command == 'all':
        return 'all'
    return _commands_dict.get(main_command)


if __name__ == '__main__':
    e = {
        "event": {
            "text": "all"
        }
    }
    print(request(e))
