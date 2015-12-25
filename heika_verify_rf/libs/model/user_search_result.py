class UserSearchResult:
    def __init__(self):
        self.user_id = ''
        self.nick_name = ''
        self.real_name = ''
        self.mobile = ''
        self.id_no = ''
        self.channel = ''
        self.verify_user_status = ''
        self.operator = ''
        self.operate_time = ''

    def __eq__(self, other):
        return self.user_id == other.user_id and self.nick_name == other.nick_name and self.real_name == other.real_name and self.mobile == other.mobile and self.id_no == other.id_no and self.channel == other.channel and self.verify_user_status == other.verify_user_status and self.operator == other.operator and self.operate_time == other.operate_time

