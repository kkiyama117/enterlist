import os
from pathlib import Path

import gspread
# from dotenv.main import find_dotenv, load_dotenv
from oauth2client.service_account import ServiceAccountCredentials

# load_dotenv(find_dotenv())

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']


class GetDataManager:
    def __init__(self):
        _json_file = Path(__file__).parent / 'gspread.json'
        _credentials = ServiceAccountCredentials.from_json_keyfile_name(_json_file, scope)
        client = gspread.authorize(_credentials)
        _file_id = os.getenv('GSPREAD_SHEET')
        self._gfile = client.open_by_key(_file_id)
        self._enterlist = self._gfile.worksheet('①エンターリスト')
        self._interview = self._gfile.worksheet('⑦面談CSV貼付')
        self._mentor = self._gfile.worksheet('メンター')
        # list used by sort
        self.check_col = self._enterlist.find('チェック').col
        self.first_contact_check_col = self._enterlist.find('エンターへ初回連絡').col
        self.add_info_check_col = self._enterlist.find('定性情報\n入力').col
        _checked_cells = self._enterlist.findall("済")
        self._checked_rows = [x.row for x in _checked_cells if x.col is self.check_col]
        self._first_contact_checked_rows = [x.row for x in _checked_cells if x.col is self.first_contact_check_col]
        self._add_info_checked_rows = [x.row for x in _checked_cells if x.col is self.add_info_check_col]

    # All sheets
    def get_enter_data(self, row: int):
        # initialize
        _row = row
        _enter_id = self._enterlist.cell(row, 1).value

        # enterlist sheets
        keys_data = {'name': '氏名', 'univ': '大学', 'department': '学部学科', 'gender': '性別'}
        needed_dict = {k: self._enterlist.cell(_row, self._enterlist.find(v).col).value for k, v in keys_data.items()}
        _row = self._interview.find(_enter_id).row
        # 面談CSV
        keys_data = {'interview': 'AD' + str(_row), 'demand': 'AG' + str(_row), 'line': 'AH' + str(_row)}
        needed_dict2 = {k: self._interview.acell(v).value for k, v in keys_data.items()}
        # 業界は複数
        industry = self._interview.acell('AE' + str(_row)).value + '/' + self._interview.acell('AF' + str(_row)).value
        # 纏める
        needed_dict = {**needed_dict, **needed_dict2}
        needed_dict.update(enter_id=_enter_id, industry=industry)
        return needed_dict

    # mentor sheet===============================================
    def get_mentors_data(self):
        return {_name: _id for _name, _id in zip(self._mentor.col_values(1), self._mentor.col_values(2)) if
                _id is not ''}

    # Enterlist sheet===================================
    def _get_enter_id(self, row: int):
        _col = self._enterlist.find('エンターID').col
        return self._enterlist.cell(row, _col).value

    def _enter_rows_with_mentor(self, mentor_name: str, sort_list: list = None):
        """条件に合ったエンターの行をListで返す(template)"""
        mentor_rows = (x.row for x in self._enterlist.findall(mentor_name))
        if sort_list is None:
            sort_list = self._checked_rows
        mentor_rows = set(mentor_rows) - set(sort_list)
        return list(mentor_rows)

    # checked
    def enter_rows_not_checked(self, mentor_name):
        return self._enter_rows_with_mentor(mentor_name, self._checked_rows)

    def enter_rows_not_first_contact(self, mentor_name):
        return self._enter_rows_with_mentor(mentor_name, self._first_contact_checked_rows)

    def enter_rows_not_add_info(self, mentor_name):
        return self._enter_rows_with_mentor(mentor_name, self._add_info_checked_rows)

    def check_enter(self, row, col):
        """Add check to enter sheet"""
        self._enterlist.update_cell(row, col, "済")


if __name__ == '__main__':
    m = GetDataManager()
    for i, j in m.get_mentors_data().items():
        print(m._enter_rows_with_mentor(i))
