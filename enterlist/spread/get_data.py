import os
from pathlib import Path

import gspread
# from dotenv.main import find_dotenv, load_dotenv
from oauth2client.service_account import ServiceAccountCredentials

# load_dotenv(find_dotenv())
from spread.models import Enter

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']


class GetDataManager:
    def __init__(self):
        _json_file = Path(__file__).parent / 'gspread.json'
        _credentials = ServiceAccountCredentials.from_json_keyfile_name(_json_file, scope)
        client = gspread.authorize(_credentials)
        _file_id = os.getenv('GSPREAD_SHEET')
        self._gfile = client.open_by_key(_file_id)
        self.enterlist = self._gfile.worksheet('①エンターリスト')
        self.interview = self._gfile.worksheet('⑦面談CSV貼付')
        self.mentor = self._gfile.worksheet('メンター')

    def get(self, row: int):
        return self.create_enter(row)

    def get_all(self, slack_id: str):
        data_all = self.find_enter_ids_with_mentor(self.find_mentor_name(slack_id))
        return data_all

    # Utils===============================================
    def find_mentor_name(self, member_id: str) -> str:
        mentor_cell = self.mentor.find(member_id)
        return self.mentor.cell(mentor_cell.row, 1).value

    def create_enter(self, row: int = None, enter_id=None):
        # initialize
        if row is not None:
            _row = row
            _enter_id = self.enterlist.cell(row, 1).value
        elif enter_id is not None:
            _enter_id = enter_id
            _row = self.enterlist.find(enter_id).row
        else:
            raise ValueError('Please set row or enter_id')

        # enterlist sheets
        keys_data = {'name': '氏名', 'univ': '大学', 'department': '学部学科', 'gender': '性別'}
        needed_dict = {k: self.enterlist.cell(row, self.enterlist.find(v).col).value for k, v in keys_data.items()}
        _row = self.interview.find(_enter_id).row
        # 面談CSV
        keys_data = {'interview': 'AD' + str(_row), 'demand': 'AG' + str(_row), 'line': 'AH' + str(_row)}
        needed_dict2 = {k: self.interview.acell(v).value for k, v in keys_data.items()}
        # 業界は複数
        industry = self.interview.acell('AE' + str(_row)).value + '/' + self.interview.acell('AF' + str(_row)).value
        # 纏める
        needed_dict = {**needed_dict, **needed_dict2}
        needed_dict.update(enter_id=_enter_id, industry=industry)
        return Enter(**needed_dict)

    # for check one row===================================
    def get_enter_id(self, row: int):
        return self.enterlist.cell(row, 1).value

    # for check all===================================
    def find_rows_with_mentor(self, mentor_name: str):
        mentor_cells = self.enterlist.findall(mentor_name)
        return [mentor_cell.row for mentor_cell in mentor_cells]

    def find_enter_ids_with_mentor(self, mentor_name: str):
        return [self.get_enter_id(i) for i in self.find_rows_with_mentor(mentor_name)]


if __name__ == '__main__':
    manager = GetDataManager()
    print(manager.get_all("U4L4PPWAK"))
