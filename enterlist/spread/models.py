import json


class Enter:
    def __init__(self, enter_id: str, name: str, univ: str, department: str,
                 gender: str, interview: str, industry: str, demand: str, line: str):
        self.enter_id = enter_id
        self.name = name
        self.univ = univ
        self.department = department
        self.gender = gender
        self.interview = interview
        self.industry = industry
        self.demand = demand
        self.line = line

    def __str__(self):
        return self.enter_id

    def detail(self) -> str:
        text: str = f'名前: {self.name} \n 学部: {self.department} \n' \
            f'性別: {self.gender} \n' \
            f'希望面談内容: {self.interview} \n' \
            f'志望業界: {self.industry} \n' \
            f'メンターへの希望: {self.demand} \n' \
            f'LINE ID: {self.line}'
        return text


def format_enter(enter):
    if type(enter) is Enter:
        text = enter.detail()
        text = 'エンターをチェックしました\n' + text
    elif type(enter) is list:
        text = ""
        for _enter in enter:
            text += _enter.detail()
        text = f'{len(enter)}人分のエンターをチェックしました\n' + text
    return text
