class Enter:
    def __init__(self, enter_id: str, name: str, univ: str, department: str,
                 gender: str, interview: str, industry: str, demand: str, line: str, checked: bool = False):
        self.enter_id = enter_id
        self.name = name
        self.univ = univ
        self.department = department
        self.gender = gender
        self.interview = interview
        self.industry = industry
        self.demand = demand
        self.line = line
        self._checked = checked

    def __str__(self):
        return self.enter_id

    def check(self):
        self._checked = True

    @property
    def checked(self):
        return self.checked

    def detail(self) -> str:
        text: str = f'名前: {self.name} \n 学部: {self.department} \n' \
            f'性別: {self.gender} \n' \
            f'希望面談内容: {self.interview} \n' \
            f'志望業界: {self.industry} \n' \
            f'メンターへの希望: {self.demand} \n' \
            f'LINE ID: {self.line}'
        return text


class Mentor:
    def __init__(self, name: str, slack_id):
        self._name = name
        self._slack_id = slack_id
