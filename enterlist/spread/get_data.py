import os
from pathlib import Path

import gspread
from dotenv import find_dotenv, load_dotenv
from oauth2client.service_account import ServiceAccountCredentials


def get_personal_data():
    load_dotenv(find_dotenv())
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']

    json_file = Path(__file__).parents[2] / 'data' / 'gspread.json'
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        json_file, scope)
    client = gspread.authorize(credentials)
    file_id = os.getenv('GSPREAD_SHEET')
    gfile = client.open_by_key(file_id)
    worksheet = gfile.sheet1

    worksheet.update_acell('A1', 'Hello World!')
    answer1 = worksheet.acell('A1')
    return answer1


if __name__ == '__main__':
    get_personal_data()
