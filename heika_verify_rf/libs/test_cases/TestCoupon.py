# -*- coding: utf-8 -*-

from ..request_utils import coupon
from ..DB_utils import utils
from .. import helper
import datetime
import time
from nose import tools


class TestCoupon:

    def __init__(self):
        self.request = None
        self.coupon_name = None
        self.nick_name = None
        self.user_key = None
        self.job_class_name = 'systemGrantCouponJob'

    def setup(self):
        self.request = coupon.CouponRequest('http://172.16.2.111:9722')
        self.request.login()
        self.coupon_name = 'test_at123'
        self.nick_name = 'rrd_10'
        self.user_key = utils.get_user_key_by_nick_name(self.nick_name)

    def teardown(self):
        utils.delete_coupon_batch_by_name(self.coupon_name)
        utils.delete_user_from_system_grant_coupon(self.user_key)
        utils.delete_all_system_grant_coupon()

    def test_create_coupon_batch(self):
        now = datetime.datetime.now()
        three_days_later = now + datetime.timedelta(days=3)
        response = self.request.create_fixed_time_system_coupon_batch(self.coupon_name, 12, 1000,
                                                                      now.strftime('%Y-%m-%d'),
                                                                      three_days_later.strftime('%Y-%m-%d'))
        assert response.text is not None
        helper.log(response.text)

        batch_key = utils.get_coupon_batch_key_by_name(self.coupon_name)
        batch_id = utils.get_coupon_batch_id_by_name(self.coupon_name)
        assert batch_key is not None
        assert batch_id is not None
        helper.log("batch_key: " + batch_key)
        helper.log("batch_id: " + str(batch_id))
        helper.log("Get batch from request")
        response = self.request.get_coupon_batch_detail(batch_id)
        coupon_batch_response = response.json()['data']['rows']
        helper.log(coupon_batch_response)

        tools.eq_(coupon_batch_response['batchStatus'], 1)
        tools.eq_(coupon_batch_response['couponsAmount'], 12.0)
        tools.eq_(coupon_batch_response['couponsCnt'], 1000)
        tools.eq_(coupon_batch_response['department'], 'MARKETING')
        tools.eq_(coupon_batch_response['grantType'], 'SYSTEM')
        tools.eq_(coupon_batch_response['id'], batch_id)
        tools.eq_(coupon_batch_response['name'], self.coupon_name)
        tools.eq_(coupon_batch_response['startTime'], now.strftime('%Y-%m-%d'))
        tools.eq_(coupon_batch_response['endTime'], three_days_later.strftime('%Y-%m-%d'))
        tools.eq_(coupon_batch_response['type'], 'VOUCHER')
        tools.eq_(coupon_batch_response['userScope'], ['ALL_TYPES'])

        response = self.request.get_coupon_receive_detail(batch_id)
        coupon_receive_detail_response = response.json()['data']['rows']
        tools.eq_(len(coupon_receive_detail_response), 0)


    def test_system_coupon_grant(self):
        now = datetime.datetime.now()
        three_days_later = now + datetime.timedelta(days=3)
        response = self.request.create_fixed_time_system_coupon_batch(self.coupon_name, 12, 1000,
                                                                      now.strftime('%Y-%m-%d'),
                                                                      three_days_later.strftime('%Y-%m-%d'))
        assert response.text is not None
        batch_key = utils.get_coupon_batch_key_by_name(self.coupon_name)
        batch_id = utils.get_coupon_batch_id_by_name(self.coupon_name)
        register_time = utils.get_start_time_in_coupon_activity_by_batch_key(batch_key) + datetime.timedelta(seconds=1)
        helper.log(register_time.strftime('%Y-%m-%d %H:%M:%S'))

        user_key = utils.get_user_key_by_nick_name(self.nick_name)
        utils.update_user_register_time_to_current_by_user_key(register_time.strftime('%Y-%m-%d %H:%M:%S'), user_key)
        utils.populate_user_into_system_grant_coupon(user_key)

        wait_time_for_job = utils.get_job_interval_time_by_job_class_name(self.job_class_name)
        time.sleep(wait_time_for_job/1000)

        response = self.request.get_coupon_receive_detail(batch_id)
        user_entry = utils.get_user_entry_by_user_key(user_key)
        coupon_receive_detail_response = response.json()['data']['rows']
        tools.eq_(len(coupon_receive_detail_response), 1)
        tools.eq_(coupon_receive_detail_response[0]['couponsStatus'], 'UNUSED')
        tools.eq_(coupon_receive_detail_response[0]['startTime'], now.strftime('%Y-%m-%d'))
        tools.eq_(coupon_receive_detail_response[0]['endTime'], three_days_later.strftime('%Y-%m-%d'))
        tools.eq_(coupon_receive_detail_response[0]['userId'], user_entry[0])
        tools.eq_(coupon_receive_detail_response[0]['mobile'], user_entry[6])
        tools.eq_(coupon_receive_detail_response[0]['nickName'], self.nick_name)

