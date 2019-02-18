import gspread
from oauth2client.service_account import ServiceAccountCredentials


def get_personal_data():
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        '../gspread.json', scope)
    gc = gspread.authorize(credentials)
    wks = gc.open_by_key('19DsLifB7GZcA13NdroXPWpS9WtUIcgy6KcidC6wGhOY').sheet1

    wks.update_acell('A1', 'Hello World!')
    answer1 = wks.acell('C3')
    return answer1
