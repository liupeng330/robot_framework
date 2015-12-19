import requests
from .. import global_config


class RequestUtil(object):
    def __init__(self, base_URL, username=None, password=None):
        self.base_URL = base_URL
        self.username = username
        self.password = password
        self.headers = {}

        if self.username is None:
            self.username = 'admin@renrendai.com'
            self.password = global_config.login_username_passwd_mapping.get(self.username)
        elif self.password is None:
            self.password = global_config.login_username_passwd_mapping.get(self.username)

    def login(self):
        post_data = {"username": self.username, "password": self.password}
        response = requests.post(self.base_URL + "/login/login", data=post_data)
        response.raise_for_status()
        self.headers["Cookie"] = "JSESSIONID=" + response.cookies.get("JSESSIONID")

    def init_user_from_mobile(self, user_id):
        post_data = {"userId": user_id}
        response = requests.post(self.base_URL + "/init", data=post_data)
        response.raise_for_status()
        return response

    def commit_user_from_mobile(self, user_id):
        post_data = {"userId": user_id}
        response = requests.post(self.base_URL + "/commit", data=post_data)
        response.raise_for_status()
        return response

    def commit_to_first_verify(self, user_id, online_time, note, **investigate_results):
        post_data = {"onlineTime": online_time, "note": note, "userId": user_id}
        post_data.update(investigate_results)
        response = requests.post(self.base_URL + "/taskMgrInvestigate/commitToFirstVerify", data=post_data, headers=self.headers)
        response.raise_for_status()
        return response

    def commit_to_second_verify(self, user_id, amount, card_product_id, cash_ratio, note):
        post_data = {"userId": user_id, "firstVerifyAmount": amount, "firstVerifyCardProductId": card_product_id, "firstCashRatio": cash_ratio, "firstVerifyNote": note}
        response = requests.post(self.base_URL + "/taskMgrVerify/commitToSecondVerify", data=post_data, headers=self.headers)
        response.raise_for_status()
        return response

    def commit_to_pass_second_verify(self, user_id, amount, card_product_id, cash_ratio, note):
        post_data = {"userId": user_id, "secondVerifyAmount": amount, "secondVerifyCardProductId": card_product_id, "secondCashRatio": cash_ratio, "secondVerifyNote": note}
        response = requests.post(self.base_URL + "/taskMgrVerify/commitToPassSecondVerify", data=post_data, headers=self.headers)
        response.raise_for_status()
        return response

    def update_verify_user(self, name, user_id, amount_limit, dept_id, role_id):
        post_date = {"userId": user_id, "name": name, "amountLimit": amount_limit, "deptId": dept_id, "roleIds": role_id}
        response = requests.post(self.base_URL + "/verifyUser/usr/update", data=post_date, headers=self.headers)
        response.raise_for_status()
        return response

    @staticmethod
    def get_all_valid_investigate_result():
        results = {'realNameInvResult': 'VALID', 'companyInvResult': 'VALID', 'workPositionInvResult': 'VALID',
                   'monthlySalaryInvResult': 'VALID', 'workPhoneInvResult': 'VALID', 'graduationInvResult': 'VALID',
                   'universityInvResult': 'VALID', 'graduateYearInvResult': 'VALID', 'marriageStatusInvResult': 'VALID',
                   'childStatusInvResult': 'VALID', 'addressInvResult': 'VALID', 'phoneInvResult': 'VALID',
                   'hasCarInvResult': 'VALID', 'hasHouseInvResult': 'VALID', 'urgentNameInvResult': 'VALID',
                   'urgentRelationInvResult': 'VALID', 'urgentMobileInvResult': 'VALID',
                   'creditCardNumberInvResult': 'VALID'}

        return results