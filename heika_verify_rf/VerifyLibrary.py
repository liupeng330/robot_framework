# -*- coding: utf-8 -*-

from libs.DB_utils.utils import *
from libs.request_utils import utils
from libs.global_enum import *
from libs.model import user_search_result
from robot.libraries.BuiltIn import BuiltIn


class VerifyLibrary(object):

    def __init__(self, base_URL, username):
        self.base_URL = base_URL
        self.username = username
        self.request_utils = utils.RequestUtil(base_URL, username)
        self.built_in = BuiltIn()

    def update_verify_user_role(self, email, dept_id, role_id, amount_limit=1000):
        real_name = get_verify_user_name_by_email(email)
        verify_user_id = get_verify_user_id_by_email(email)
        self.request_utils.login()
        response = self.request_utils.update_verify_user(real_name, verify_user_id, amount_limit, dept_id, role_id)
        return response.json()

    def compare_user_search_result(self, ui_row, ui_row_index, key, search_type, verify_user_status):
        ui_row_index = int(ui_row_index)
        key = key.encode('utf-8')
        search_type = search_type.encode('utf-8')
        verify_user_status = verify_user_status.encode('utf-8')

        # get user search result from DB
        if verify_user_status is None:
            self.built_in.log(key)
            search_type_enum = SearchType.get_enum(search_type)
            user_verify_status = search_user(search_type_enum, key)
        else:
            user_verify_status = search_user(SearchType.get_enum(search_type), key, VerifyUserStatus.get_enum(verify_user_status).name)
        if len(user_verify_status) - 1 < ui_row_index:
            raise AssertionError('User search result from DB has count %s, but you want to get index %s' % (len(user_verify_status), ui_row_index))

        self.built_in.log('Start to fetch from DB')
        user_verify_status_index = user_verify_status[ui_row_index]
        usr_DB = user_search_result.UserSearchResult()
        usr_DB.user_id = unicode(user_verify_status_index[0])
        usr_DB.nick_name = user_verify_status_index[1]
        usr_DB.real_name = user_verify_status_index[2]
        usr_DB.mobile = user_verify_status_index[3]
        usr_DB.id_no = user_verify_status_index[4]
        usr_DB.channel = unicode(Channel.get_value(user_verify_status_index[5]), 'utf-8')
        usr_DB.verify_user_status = unicode(VerifyUserStatus.get_value(user_verify_status_index[6]), 'utf-8')
        if usr_DB.verify_user_status == u'等待提交' or usr_DB.verify_user_status == u'等待调查':
            usr_DB.operator = ''
            usr_DB.operate_time = ''
        else:
            (operator, operate_time) = get_latest_verify_user_status_log(usr_DB.user_id)
            usr_DB.operator = operator
            usr_DB.operate_time = unicode(operate_time.strftime('%Y-%m-%d %H:%M'), 'utf-8')

        self.built_in.log('Start to fetch from UI')
        usr_UI = user_search_result.UserSearchResult()
        usr_UI.user_id = ui_row['userId']
        usr_UI.nick_name = ui_row['nickName']
        usr_UI.real_name = ui_row['realName']
        usr_UI.mobile = ui_row['mobile']
        usr_UI.id_no = ui_row['idNo']
        usr_UI.channel = ui_row['userType']
        usr_UI.verify_user_status = ui_row['verifyUserStatus']
        usr_UI.operator = ui_row['operator']
        usr_UI.operate_time = ui_row['operateTime']

        self.built_in.log('Start to compare them')
        if usr_DB == usr_UI:
            return
        else:
            raise AssertionError('User search result from DB and UI are different for row index %s !!' % ui_row_index)

    def update_verify_user_status(self, user_id, verify_user_status):
        if verify_user_status == VerifyUserStatus.UNCOMMIT:
            update_user_to_uncommit_status(user_id)
            return
        if verify_user_status == VerifyUserStatus.INQUIREING:
            update_user_to_inquireing_status(user_id)
            return
        if verify_user_status == VerifyUserStatus.INQUIRE_SUCCESS:
            update_user_to_inquire_success_status(user_id, 1, 'investigate note', 12)
            return


if __name__ == "__main__":
    verify_library = VerifyLibrary('http://172.16.2.38:15081', 'admin@renrendai.com')
    verify_library.update_verify_user_role('auto_permission_tes@rernedai.com', 26, 12)
    verify_library.compare_user_search_result({'userType': u'\u666e\u901a\u7528\u6237', 'idNo': u'130521199307091000', 'operateTime': u'2015-12-08 15:45', 'verifyUserStatus': u'\u7b49\u5f85\u4e00\u5ba1', 'realName': u'\u65bd\u65ed\u5b81', 'mobile': u'13146865530', 'nickName': u'auto_01', 'userId': u'100034832', 'operator': u'\u5218\u9e4f\u6d4b\u8bd5'},
                                              0,
                                              'auto')
