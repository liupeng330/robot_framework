from ..request_utils import coupon
from ..helper import *

class TestCoupon:

    def __init__(self):
        self.request = None

    def setup(self):
        self.request = coupon.CouponRequest('http://172.16.2.111:9722')
        self.request.login()

    def test_create_coupon(self):
        response = self.request.create_fixed_time_system_coupon_batch('test_at4', 12, 1000, '2015-12-19', '2015-12-20')
        log(response.text)

