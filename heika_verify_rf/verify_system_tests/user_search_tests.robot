*** Settings ***
Test Setup       Open Browser To Login Page
Test Teardown    Close Browser
Resource    ../resources/resource.robot
Library     String
Library      ../VerifyLibrary.py   http://${SERVER}    ${ADMIN USER}
Test Template    Search user test

*** Test Cases ***
Test One        后台
Test two        auto

*** Keywords ***
Search user test
    [Arguments]     ${key}
    Login With Valid Account    ${ADMIN USER}   ${ADMIN PASSWORD}
    Click TreeNode		 用户查询
    Page Title Visible   用户查询
    Select Frame   ${USER SEARCH IFRAME}
    Input Text     id=oText    ${key}
    Click Button   id=oSubmit
    Wait Until Page Contains Element    ${USER SEARCH TABLE}

    ${row_count} =      Get Table Row Count   ${USER SEARCH TABLE}
    Log     共有行数：${row_count}

    : FOR    ${i}   IN RANGE    ${row_count}
    \   ${row} =       Get User Search Results     ${USER SEARCH TABLE}    ${i}
    \   Log     第${i}行：${row}
    \   Compare User Search Result      ${row}      ${i}       ${key}
