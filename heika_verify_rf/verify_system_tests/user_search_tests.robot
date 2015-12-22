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
    Select Frame   ${USER SEARCH IFRAME}
    Input Text     id=oText    后台
    Click Button   id=oSubmit
    Wait Until Page Contains Element  xpath=//*[@id="tabs"]/div[2]/div/div/div/div/div[2]/div[2]/div[2]/table
#    ${cell} =   Get Table Cell  xpath=//*[@id="tabs"]/div[2]/div/div/div/div/div[2]/div[2]/div[2]/table   1   3
#    Log     ${cell}
    ${row_count} =      Get Table Row Count  xpath=//*[@id="tabs"]/div[2]/div/div/div/div/div[2]/div[2]/div[2]/table
    Log     ${row_count}
    &{all cell} =       Get User Search Results   xpath=//*[@id="tabs"]/div[2]/div/div/div/div/div[2]/div[2]/div[2]/table     0
    log     &{all cell}[userType]
