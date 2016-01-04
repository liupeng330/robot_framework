*** Settings ***
Resource    ../resources/resource.robot
Library      ../VerifyCoupon.py
Test Setup  my setup
Test Teardown  my cleanup


*** Test Cases ***
Test create fixed time coupon batch
    create fixed time coupon batch

Test create fixed length coupon batch
    create fixed length coupon batch

Test system fixed time coupon grant
    system fixed time coupon grant

Test system fixed length coupon grant
    system fixed length coupon grant

Test disable and in time range system fixed length coupon grant
    disable and in time range system fixed length coupon grant

Test disable and not in time range system fixed length coupon grant
    disable and not in time range system fixed length coupon grant

Test disable and in time range system fixed time coupon grant
    disable and in time range system fixed time coupon grant

Test disable and not in time range system fixed time coupon grant
    disable and not in time range system fixed time coupon grant
