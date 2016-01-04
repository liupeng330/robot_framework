*** Settings ***
#Test Setup       Open Browser To Login Page
#Test Teardown    Close Browser
Suite Setup     cleanup task by executor names   刘鹏测试   刘鹏测试2   刘鹏测试3
Resource    ../resources/resource.robot
Library     String
Library      ../VerifyLibrary.py   http://${SERVER}    ${ADMIN USER}    ${DUBBO WEB API URL}
Test Template    Flow Task By People For Inquireing

*** Test Cases ***
Test1 Flow Task By People For Inquireing     刘鹏测试    auto_01
Test2 Flow Task By People For Inquireing     刘鹏测试2    auto_02
Test3 Flow Task By People For Inquireing     刘鹏测试3    auto_03

*** Keywords ***
Flow Task By People For Inquireing
    [Arguments]     ${verify user real name}  ${task_nick_name}
    cleanup task by executor names   ${verify user real name}
    flow setup by people for inquireing   ${verify user real name}
    populate task by nick names  ${task_nick_name}
    verify pending job  ${verify user real name}    ${task_nick_name}  首次调查
