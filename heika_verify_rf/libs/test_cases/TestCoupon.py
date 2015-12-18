# -*- coding: utf-8 -*-

from ..request_utils import coupon
from ..DB_utils import utils
from .. import helper
import datetime
from nose import tools


class TestCoupon:

    def __init__(self):
        self.request = None
        self.coupon_name = None
        self.nick_name = None
        self.user_key = None

    def setup(self):
        self.request = coupon.CouponRequest('http://172.16.2.111:9722')
        self.request.login()
        self.coupon_name = 'test_at123'
        self.nick_name = '审核测试1'
        self.user_key = utils.get_user_key_by_nick_name(self.nick_name)

    def teardown(self):
        utils.delete_coupon_batch_by_name(self.coupon_name)
        utils.delete_user_from_system_grant_coupon(self.user_key)
        utils.delete_all_system_grant_coupon()

    def test_create_coupon(self):
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

        # utils.populate_user_into_system_grant_coupon(self.user_key)
