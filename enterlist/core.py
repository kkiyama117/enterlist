from models import Enter
from spread import GetDataManager
from utils import post_message_to_channel

_spread_api = GetDataManager()
_first_message = '以下のエンター情報を読んで内容を確認して下さい'


def confirm_enters_data(user_id: str):
    post_message_to_channel(user_id, 'CONFIRM START')
    # mentor 毎に
    for _name, _id in _spread_api.get_mentors_data().items():
        post_message_to_channel(_id, _first_message)
        # 該当するenterの行をゲット
        for row in _spread_api.enter_rows_not_checked(_name):
            # Enter の model
            enter = Enter(**(_spread_api.get_enter_data(row)))
            # slack に投稿
            post_message_to_channel(_id, enter.detail())
            # 確認済みのチェックを入れる
            _spread_api.check_enter(row, _spread_api.check_col)
        _last_message = '上記のエンターについては, spreadsheetに自動でチェックが入りました'
        post_message_to_channel(_id, _last_message)
    post_message_to_channel(user_id, 'CONFIRM END')
    return "CONFIRM ENTERS DATA TO MENTORS"


if __name__ == '__main__':
    confirm_enters_data("")
