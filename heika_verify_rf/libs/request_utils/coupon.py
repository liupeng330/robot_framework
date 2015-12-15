import requests
import utils


class CouponRequest(utils.RequestUtil):

    def create_coupon_batch(self, name, department, discount_type, amount, coupon_count, user_scope, time_type, start_time, end_time, validity_period, validity_type, grant_type, active_action):
        post_data = {"name": name,
                     "department": department,
                     "discountType": discount_type,
                     "amount": amount,
                     "couponsCnt": coupon_count,
                     "userScope": user_scope,
                     "timeType": time_type,
                     "startTime": start_time,
                     "endTime": end_time,
                     "validityPeriod": validity_period,
                     "validityType": validity_type,
                     "grantType": grant_type}
        if grant_type == 'SYSTEM':
            post_data["activeAction"] = active_action
        response = requests.post(self.base_URL + "/coupons/addBatch", data=post_data, headers=self.headers)
        response.raise_for_status()
        return response

    def create_fixed_time_coupon_batch(self, name, amount, coupon_count, start_time, end_time, grant_type, active_action):
        return self.create_coupon_batch(name, 'MARKETING', 'FIXED_VALUE', amount, coupon_count, 'ALL_TYPES',
                                        'FIXED_TIME_PERIOD', start_time, end_time, 0, 'DAY', grant_type, active_action)

    def create_fixed_length_coupon_batch(self, name, amount, coupon_count, validity_period, validity_type, grant_type, active_action):
        return self.create_coupon_batch(name, 'MARKETING', 'FIXED_VALUE', amount, coupon_count, 'ALL_TYPES',
                                        'FIXED_LENGTH', '', '', validity_period, validity_type, grant_type, active_action)

    def create_fixed_time_system_coupon_batch(self, name, amount, coupon_count, start_time, end_time):
        return self.create_fixed_time_coupon_batch(name, amount, coupon_count, start_time, end_time, 'SYSTEM', 'REGISTER_VERIFY')

    def create_fixed_length_system_coupon_batch(self, name, amount, coupon_count, validity_period, validity_type):
        return self.create_fixed_length_coupon_batch(name, amount, coupon_count, validity_period, validity_type, 'SYSTEM', 'REGISTER_VERIFY')

    def create_fixed_time_manual_coupon_batch(self, name, amount, coupon_count, start_time, end_time):
        return self.create_fixed_time_coupon_batch(name, amount, coupon_count, start_time, end_time, 'MANUAL', '')

    def create_fixed_length_manual_coupon_batch(self, name, amount, coupon_count, validity_period, validity_type):
        return self.create_fixed_length_coupon_batch(name, amount, coupon_count, validity_period, validity_type, 'MANUAL', '')
