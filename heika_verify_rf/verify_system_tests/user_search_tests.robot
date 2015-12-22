*** Settings ***
Test Setup       Open Browser To Login Page
Test Teardown    Close Browser
Resource    ../resources/resource.robot
Library     String
Library      ../VerifyLibrary.py   http://${SERVER}    ${ADMIN USER}

*** Test Cases ***
Search user test
    Login With Valid Account    ${ADMIN USER}   ${ADMIN PASSWORD}
    Click TreeNode		 用户查询
    Page Title Visible   用户查询
    Select Frame   ${IFRAME}
    Input Text     id=oText    123123
    Click Button   id=oSubmit
    ${cell} =   get table cell  xpath=//*[@id="tabs"]/div[2]/div/div/div/div/div[2]/div[2]/div[2]/table   1   3
    Log     ${cell}
    ${row_count} =      get table row count  xpath=//*[@id="tabs"]/div[2]/div/div/div/div/div[2]/div[2]/div[2]/table
    Log     ${row_count}
