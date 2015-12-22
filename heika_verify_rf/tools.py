# -*- coding: utf-8 -*-  
import sys

import libs.helper
from libs.DB_utils.utils import *
from libs.request_utils.utils import *
from datetime import datetime


def help_info():
    print "将指定的user_id置为待调查状态\n" \
          "\tpython tools.py init user_id列表 "


def user_login(username):
    libs.helper.log("使用用户名'%s'登陆" % username)
    request_util = RequestUtil('http://172.16.2.38:15081', username)
    request_util.login()
    return request_util


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        help_info()
        sys.exit(0)

    if sys.argv[1] == 'init':
        for user_id in sys.argv[2:]:
            request_util = RequestUtil('http://172.16.2.38:17788/dubbo/test/')
            # request_util = RequestUtil('http://172.16.2.111:7020/heika-verify/dubbo/test/')

            libs.helper.log('将user_id为%s的用户置为待调查状态' % user_id)
            init_user(user_id)

            libs.helper.log('删除审核状态表原有数据')
            delete_verify_user_status_by_user_id(user_id)

            libs.helper.log('调用接口模拟初始化审核状态')
            libs.helper.log(request_util.init_user_from_mobile(user_id))

            libs.helper.log('调用接口模拟提交审核')
            libs.helper.log(request_util.commit_user_from_mobile(user_id))
        sys.exit(0)

    if sys.argv[1] == 'cleanup_by_user_id':
        for user_id in sys.argv[2:]:
            libs.helper.log('将user_id为%s的用户任务清除' % user_id)
            verify_user_status_id = get_verify_user_status_id_by_user_id(user_id)

            if verify_user_status_id is None:
                libs.helper.log_error('未找到user_id=%s对应的verify_user_status数据' % user_id)
                pass

            libs.helper.log('verify_user_status_id = %s' % verify_user_status_id)
            libs.helper.log('删除verify_process_task表中的数据, verify_user_status_id为%s' % verify_user_status_id)
            delete_verify_process_task_by_verify_user_status_id(verify_user_status_id)
        sys.exit(0)

    if sys.argv[1] == 'cleanup_by_executor_name':
        for real_name in sys.argv[2:]:
            libs.helper.log('将real_name为%s的用户任务清除' % real_name)
            verify_user_id = get_verify_user_id_by_real_name(real_name)

            if verify_user_id is None:
                libs.helper.log_error('未找到real_name=%s的verify_user数据' % real_name)
                pass

            libs.helper.log('verify_user_id = %s' % verify_user_id)
            libs.helper.log('删除verify_process_task表中的数据, executor为%s' % verify_user_id)
            delete_verify_process_task_by_executor_id(verify_user_id)
        sys.exit(0)

    if sys.argv[1] == 'inv_pass':
        request_util = user_login(sys.argv[2])
        for user_id in sys.argv[3:]:
            libs.helper.log('将user_id为%s的用户通过调查' % user_id)
            inv_rets = request_util.get_all_valid_investigate_result()
            response = request_util.commit_to_first_verify(user_id, 12, '调查备注', **inv_rets)

            libs.helper.log(response.text)
        sys.exit(0)

    if sys.argv[1] == 'first_verify_pass':
        request_util = user_login(sys.argv[2])
        for user_id in sys.argv[3:]:
            libs.helper.log('将user_id为%s的用户通过一审' % user_id)
            response = request_util.commit_to_second_verify(user_id, 123, 3, 56, '一审备注')

            libs.helper.log(response.text)
        sys.exit(0)

    if sys.argv[1] == 'second_verify_pass':
        request_util = user_login(sys.argv[2])
        for user_id in sys.argv[3:]:
            libs.helper.log('将user_id为%s的用户通过二审' % user_id)
            response = request_util.commit_to_pass_second_verify(user_id, 321, 2, 78, '二审备注')

            libs.helper.log(response.text)
        sys.exit(0)

    if sys.argv[1].startswith('grant_coupon'):
        count_of_user = sys.argv[2]
        user_nick_name_prefix = sys.argv[3]
        register_time = sys.argv[4]
        sent_status = sys.argv[5:]
        user_keys = get_user_keys_by_nick_name_prefix(user_nick_name_prefix, count_of_user)

        time = None
        if register_time == 'current':
            time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        else:
            time = register_time

        if sys.argv[1].endswith('cleanup'):
            delete_user_from_system_grant_coupon(*user_keys)
        else:
            coupon_sent_user_keys = get_user_keys_from_system_grant_coupon(*sent_status)
            coupon_not_sent_user_keys = []
            for i in user_keys:
                if i[0] not in coupon_sent_user_keys:
                    coupon_not_sent_user_keys.append(i[0])
            update_user_register_time_to_current_by_user_key(time, *coupon_not_sent_user_keys)
            populate_user_into_system_grant_coupon(*coupon_not_sent_user_keys)

    if sys.argv[1] == 'coupon_cleanup':
        batch_name = sys.argv[2]
        if batch_name == 'all':
            delete_all_system_coupon_batch()
        else:
            delete_coupon_batch_by_name(batch_name)

