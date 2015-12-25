# -*- coding: utf-8 -*-
from enum import Enum


class SearchType(Enum):
    NickName = "昵称"
    Mobile = "手机号"
    IdNum = "身份证"
    RealName = "姓名"

    @staticmethod
    def get_enum(value):
        for i, j in SearchType.__members__.items():
            if j.value == value:
                return j
        return None


class VerifyUserStatus(Enum):
    UNCOMMIT = "等待提交"
    INQUIREING = "等待调查"
    INQUIRE_SUCCESS = "等待一审"
    VERIFY_FAIL = "补件"
    FIRST_VERIFY_SUCCESS = "等待二审"
    FIRST_SEND_BACK = "一审退回"
    SECOND_SEND_BACK = "二审退回"
    VERIFY_REJECT = "退件"
    VERIFY_SUCCESS = "审核通过"

    @staticmethod
    def get_value(key):
        for i, j in VerifyUserStatus.__members__.items():
            if i == key:
                return j.value
        return None

    @staticmethod
    def get_enum(value):
        for i, j in VerifyUserStatus.__members__.items():
            if j.value == value:
                return j
        return None


class Channel(Enum):
    BD_IMPORT = "BD渠道用户"
    PERSONAL_REGISTER = "普通用户"

    @staticmethod
    def get_value(key):
        for i, j in Channel.__members__.items():
            if i == key:
                return j.value
        return None
