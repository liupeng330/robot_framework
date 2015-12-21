from libs.DB_utils.utils import *
from libs.request_utils import utils


class VerifyLibrary(object):

    def __init__(self, base_URL, username):
        self.base_URL = base_URL
        self.username = username
        self.request_utils = utils.RequestUtil(base_URL, username)

    def update_verify_user_role(self, email, dept_id, role_id, amount_limit=1000):
        real_name = get_verify_user_name_by_email(email)
        verify_user_id = get_verify_user_id_by_email(email)
        self.request_utils.login()
        response = self.request_utils.update_verify_user(real_name, verify_user_id, amount_limit, dept_id, role_id)
        return response.json()


if __name__ == "__main__":
    verify_library = VerifyLibrary('http://172.16.2.38:15081', 'admin@renrendai.com')
    verify_library.update_verify_user_role('auto_permission_tes@rernedai.com', 26, 12)
