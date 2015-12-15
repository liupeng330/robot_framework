# -*- coding: utf-8 -*-

import mysql.connector
import libs.global_config
import libs.helper
from datetime import datetime

conn = mysql.connector.connect(
    user=libs.global_config.db_user_name,
    password=libs.global_config.db_password,
    host=libs.global_config.db_host,
    port=libs.global_config.db_port,
    database=libs.global_config.db_database,
    charset='utf8')
cursor = conn.cursor()


def commit(query):
    try:
        cursor.execute(query)
        conn.commit()
        libs.helper.log("执行sql语句：\n%s\n影响行数：%d\n" % (query, cursor.rowcount))
        return cursor.rowcount
    except Exception, e:
        libs.helper.log_error('\n\n执行sql语句%s时出错: %s，回滚\n' % (query, e))
        conn.rollback()


def fetch_one(query):
    cursor.execute(query)
    ret = cursor.fetchone()
    if ret is not None and len(ret) > 0:
        return ret[0]
    return None


def get_all_user():
    query = 'select * from user'
    cursor.execute(query)
    return cursor.fetchall()


def get_user_id_by_nick_name(nick_name):
    cursor.execute("select * from user where nick_name = '%s' " % nick_name)
    ret = cursor.fetchone()
    if ret is not None:
        return ret[0]
    return None


def get_verify_user_id_by_email(email):
    cursor.execute("select id from verify_user where email = '%s' " % email)
    ret = cursor.fetchone()
    if ret is not None:
        return ret[0]
    return None


def get_verify_user_name_by_email(email):
    cursor.execute("select real_name from verify_user where email = '%s' " % email)
    ret = cursor.fetchone()
    if ret is not None:
        return ret[0]
    return None


def get_dept_id_by_dept_name(dept_name):
    cursor.execute("select id from verify_departments where department_name = '%s' " % dept_name)
    ret = cursor.fetchone()
    if ret is not None:
        return ret[0]
    return None


def update_nick_name_by_user_id(user_id, nick_name):
    cursor.execute("update user set nick_name='%s' where user_id='%s'" % (nick_name, user_id))
    conn.commit()


def update_nick_name_by_original_nick_name(original_nick_name, nick_name):
    cursor.execute("update user set nick_name='%s' where user_id='%s'" % (nick_name, original_nick_name))
    conn.commit()


def update_nick_name(*original_nick_names):
    for nick_name in original_nick_names:
        user_id = get_user_id_by_nick_name(nick_name)
        if user_id is None:
            pass
        libs.helper.log('获取一个user_id：%d' % user_id)
        if nick_name.startswith('rrd_'):
            new_nick_name = nick_name.replace('rrd_', '审核测试')
            libs.helper.log('更新userId为%s的用户的昵称从%s更新为%s' % (user_id, nick_name, new_nick_name))
            update_nick_name_by_user_id(user_id, new_nick_name)


def get_verify_user_status_id_by_user_id(user_id):
    libs.helper.log('获取user_id为%s的verify_user_status表的主键id' % user_id)
    sql = "SELECT id from verify_user_status where user_id = %s" % user_id
    return fetch_one(sql)


def get_verify_user_id_by_real_name(real_name):
    libs.helper.log('获取real_name为%s的verify_user表的主键id' % real_name)
    sql = "SELECT id from verify_user where real_name = '%s'" % real_name
    return fetch_one(sql)


def delete_verify_user_status_by_user_id(user_id):
    libs.helper.log('删除verify_user_status表中的数据')
    delete_sql = "DELETE from verify_user_status where user_id = %s" % user_id
    commit(delete_sql)


def delete_verify_process_task_by_verify_user_status_id(id):
    libs.helper.log('按照verify_user_status_id删除verify_process_task表中的记录')
    delete_sql = "DELETE from verify_process_task where verify_user_status_id = %s" % id
    commit(delete_sql)


def delete_verify_process_task_by_executor_id(verify_user_id):
    libs.helper.log('按照executor删除verify_process_task表中的记录')
    delete_sql = "DELETE from verify_process_task where executor = %s" % verify_user_id
    commit(delete_sql)


def init_user(user_id):
    update_verify_user_status_to_inquireing(user_id)
    update_user_info_result_to_pending(user_id)
    delete_user_status_log(user_id)
    delete_strategy_output(user_id)
    delete_verify_user_info_refine(user_id)


def update_verify_user_status_to_inquireing(user_id):
    libs.helper.log('将verify_user_status表的数据置为待调查')
    update_status_sql = "UPDATE verify_user_status SET " \
                        "verify_user_status='INQUIREING'," \
                        "reject_operation=NULL," \
                        "investigate_time=NULL," \
                        "first_verify_time=NULL," \
                        "second_verify_time=NULL," \
                        "investigate_user_id=NULL," \
                        "first_verify_user_id=NULL," \
                        "second_verify_user_id=NULL," \
                        "investigate_note=NULL," \
                        "first_verify_note=NULL," \
                        "second_verify_note=NULL," \
                        "first_verify_amount=NULL," \
                        "first_verify_card_product_id=NULL," \
                        "second_verify_amount=NULL," \
                        "second_verify_card_product_id=NULL," \
                        "online_time=NULL," \
                        "reject_reason_list=NULL," \
                        "in_youxin_back_list=NULL," \
                        "first_cash_draw_ratio=NULL," \
                        "cash_draw_ratio=NULL," \
                        "version='0' " \
                        "WHERE user_id = %s" % user_id
    commit(update_status_sql)


def update_user_info_result_to_pending(user_id):
    libs.helper.log('将verify_user_info_result表置为PENDING\n')
    update_user_info_result = "UPDATE `verify_user_info_result` SET `value_` = 'PENDING' WHERE `user_id` = %s" % user_id
    commit(update_user_info_result)


def delete_user_status_log(user_id):
    libs.helper.log('将verify_user_status_log表中的数据删除\n')
    delete_user_status_log = "delete from `verify_user_status_log` where `user_id` = %s" % user_id
    commit(delete_user_status_log)


def delete_strategy_output(user_id):
    libs.helper.log('将verify_strategy_output表中的数据删除\n')
    delete_strategy_output = "delete from `verify_strategy_output` where `user_id` = %s" % user_id
    commit(delete_strategy_output)


def delete_verify_user_info_refine(user_id):
    libs.helper.log('将verify_user_info_refine表中的数据删除\n')
    delete_user_info_refine = "delete from `verify_user_info_refine` where `user_id` = %s" % user_id
    commit(delete_user_info_refine)


def get_user_keys_by_nick_name_prefix(prefix, count):
    query = "select user_key from user where nick_name like '%s' order by nick_name LIMIT %s" % (prefix + '%', count)
    cursor.execute(query)
    return cursor.fetchall()


def get_user_keys_from_system_grant_coupon(status=0):
    query = "select `user_key` from `system_grant_coupon_users` where `status` = %s" % status
    cursor.execute(query)
    return cursor.fetchall()


def populate_user_into_system_grant_coupon(*user_keys):
    for key in user_keys:
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("""INSERT INTO `system_grant_coupon_users` (`user_key`, `status`, `create_time`, `update_time`,
        `active_action`, `version`) VALUES (%s, 1, %s, %s, 'REGISTER_VERIFY', 0)""",
                       (key[0], str(now), str(now)))
        conn.commit()


def delete_user_from_system_grant_coupon(*user_keys):
    for key in user_keys:
        cursor.execute("""delete from `system_grant_coupon_users` where `user_key` = %s""", (key[0],))
        conn.commit()


def get_coupon_batch_key_by_name(name):
    cursor.execute("select batch_key from `coupon_batch` where name = %s", (name,))
    ret = cursor.fetchone()
    if ret is None:
        return None
    return ret[0]


def delete_coupon_batch_by_name(name):
    batch_key = get_coupon_batch_key_by_name(name)
    if batch_key is None:
        return
    cursor.execute("""delete from `coupon` where `coupon_batch_key` = %s""", (batch_key,))
    cursor.execute("""delete from `coupon_batch_log` where `batch_key` = %s""", (batch_key,))
    cursor.execute("""delete from `coupon_batch` where `batch_key` = %s""", (batch_key,))
    conn.commit()


