*** Settings ***
Library           Selenium2Library      2      10

*** Variables ***
${SERVER}           172.16.2.38:15081
${BROWSER}          Chrome
${DELAY}            0
${ADMIN USER}       admin@renrendai.com
${ADMIN PASSWORD}   L123456
${VALID USER}       auto_permission_tes@rernedai.com
${VALID PASSWORD}   L123456
${LOGIN URL}        http://${SERVER}/login/index.html
${WELCOME URL}      http://${SERVER}/index.html

&{ROLE NAME AND ROLE ID}     调查人员=12     审核人员=13     审核经理=14     管理员=15
&{DEPARTMENT NAME AND ID}    组织=26

${TREE TITLE ONLY NODE}     调额管理

@{TREE NODE TITLES}     用户查询    BD用户数据导入    待办任务    办结任务    我参与的进件
...                     流程任务管理  流程配置管理  修改个人信息  角色授权管理  组织人员管理

@{INV TREE NODE TITLES}     用户查询    待办任务    办结任务    我参与的进件
@{INV TREE NODE TITLES NOT VISIBLE}     流程任务管理  流程配置管理  修改个人信息  角色授权管理  组织人员管理

@{AUDIT TREE NODE TITLES}     用户查询    待办任务    办结任务    我参与的进件
@{AUDIT TREE NODE TITLES NOT VISIBLE}     流程任务管理  流程配置管理  修改个人信息  角色授权管理  组织人员管理

@{AUDIT MANAGER TREE NODE TITLES}     用户查询    待办任务    办结任务    我参与的进件    流程任务管理  流程配置管理
@{AUDIT MANAGER TREE NODE TITLES NOT VISIBLE}     修改个人信息  角色授权管理  组织人员管理

*** Keywords ***
Open Browser To Login Page
    Open Browser    ${LOGIN URL}    ${BROWSER}
    Maximize Browser Window
    Set Selenium Speed    ${DELAY}
    Login Page Should Be Open

Login Page Should Be Open
    Title Should Be    登录

Go To Login Page
    Go To    ${LOGIN URL}
    Login Page Should Be Open

Input Username
    [Arguments]    ${username}
    Input Text    username    ${username}

Input Password
    [Arguments]    ${password}
    Input Text    password    ${password}

Submit Credentials
    Click Button    loginCheck

Welcome Page Should Be Open
    Location Should Be    ${WELCOME URL}
    Title Should Be    黑卡审核系统

Login With Valid Account
    [Arguments]    ${username}  ${password}
    Input Username    ${username}
    Input Password    ${password}
    Submit Credentials
    Wait Until Keyword Succeeds        2 min       10 sec      Welcome Page Should Be Open

Click TreeNode
    [Arguments]    ${treetitle}
    Click Element   xpath=//*[@class="tree-node"]/span[@class='tree-icon tree-file icon-round']/following-sibling::span[text()="${treetitle}"]

Click TreeTitle
    [Arguments]    ${treetitle}
    click Element   xpath=//*[@id="navTree"]//span[text()="${treetitle}"]

Page Title Visible
    [Arguments]    ${pagetitle}
    Wait Until Element Is Visible   xpath=//*[@id="main-center"]//span[@class="tabs-title tabs-closable" and text()="${pagetitle}"]

TreeNode Not Visble
    [Arguments]    ${treetitle}
    Wait Until Element Is Not Visible   xpath=//*[@class="tree-node"]/span[@class='tree-icon tree-file icon-round']/following-sibling::span[text()="${treetitle}"]

TreeTitle Not Visble
    [Arguments]    ${treetitle}
    Wait Until Element Is Not Visible   xpath=//*[@id="navTree"]//span[text()="${treetitle}"]
