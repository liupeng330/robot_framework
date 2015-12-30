*** Settings ***
Test Setup       Open Browser To Login Page
Test Teardown    Close Browser
Resource    ../resources/resource.robot
Library     String
Library      ../VerifyLibrary.py   http://${SERVER}    ${ADMIN USER}
Test Template    Search user test

*** Test Cases ***
Test Search By Nick Name And Uncommit        昵称      等待提交    auto_01    100034832
Test Search By Nick Name And Inquireing        昵称     等待调查   auto_01    100034832
Test Search By Nick Name And Inquire Success       昵称     等待一审   auto_01    100034832
Test Search By Mobile And Uncommit        手机号    等待提交    13146865530    100034832
Test Search By Mobile And Inquireing        手机号   等待调查    13146865530    100034832
Test Search By Mobile And Inquire Success        手机号    等待一审      13146865530    100034832
Test Search By IdNo And Uncommit        身份证    等待提交    130521199307091000    100034832
Test Search By IdNo And Inquireing        身份证    等待调查       130521199307091000    100034832
Test Search By IdNo And Inquire Success        身份证    等待一审         130521199307091000    100034832
Test Search By Real Name Uncommit        姓名      等待提交    施旭宁    100034832
Test Search By Real Name Inquireing        姓名      等待调查         施旭宁    100034832
Test Search By Real Name Inquire Success        姓名    等待一审      施旭宁    100034832

*** Keywords ***
Search user test
    [Arguments]     ${search key}  ${verify status}  ${key}  ${user id}
    Login With Valid Account    ${ADMIN USER}   ${ADMIN PASSWORD}
    Click TreeNode		 用户查询
    Page Title Visible   用户查询
    Select Frame   ${USER SEARCH IFRAME}
    Run Keyword If      '${search key}' == '昵称'     User Search Select By NickName
    Run Keyword If      '${search key}' == '手机号'    User Search Select By Mobile
    Run Keyword If      '${search key}' == '身份证'    User Search Select By IdNo
    Run Keyword If      '${search key}' == '姓名'     User Search Select By RealName
    Update Verify User Status   ${user id}      ${verify status}
    Run Keyword If      '${verify status}' == '等待提交'      User Search Select By UNCOMMIT Status
    Run Keyword If      '${verify status}' == '等待调查'      User Search Select By INQUREING Status
    Run Keyword If      '${verify status}' == '等待一审'      User Search Select By INQUIRE_SUCCESS Status
    Input Text     id=oText    ${key}
    Click Button   id=oSubmit
    Wait Until Page Contains Element    ${USER SEARCH TABLE}

    ${row_count} =      Get Table Row Count   ${USER SEARCH TABLE}
    Log     共有行数：${row_count}
    should be equal as integers     ${row_count}    1       应该只搜索到一条数据

    : FOR    ${i}   IN RANGE    ${row_count}
    \   ${row} =       Get User Search Results     ${USER SEARCH TABLE}    ${i}
    \   Log     第${i}行：${row}
    \   Compare User Search Result      ${row}      ${i}       ${key}   ${search key}   ${verify status}
