*** Settings ***
Test Setup     cleanup task by executor names   刘鹏测试   刘鹏测试2   刘鹏测试3
Resource    ../resources/resource.robot
Library     String
Library      ../VerifyLibrary.py   http://${SERVER}    ${ADMIN USER}    ${DUBBO WEB API URL}

*** Test Cases ***
Test Flow Task By People For Inquireing
    log     设置首次调查的人员
    flow setup by people for inquireing   刘鹏测试  刘鹏测试2   刘鹏测试3

    log     产生新的进件
    populate task by nick names  auto_01    auto_02    auto_03

    log     验证分配到首次调查的进件
    verify pending job  刘鹏测试    auto_01     首次调查
    verify pending job  刘鹏测试2    auto_02     首次调查
    verify pending job  刘鹏测试3    auto_03     首次调查

Test Flow Task By People For First Verify
    log     设置首次调查的人员
    flow setup by people for inquireing   刘鹏测试  刘鹏测试2   刘鹏测试3

    log     设置一审的人员
    flow setup by people for inquire success  刘鹏测试  刘鹏测试2   刘鹏测试3

    log     分配首次调查的进件
    populate task by nick names  auto_01    auto_02    auto_03

    log     将auto_01调查通过
    commit to first verify   刘鹏测试  auto_01
    log     验证auto_01分配到了一审，其他进件依然在首次调查节点
    verify pending job  刘鹏测试    auto_01     待一审
    verify done job  刘鹏测试    auto_01     首次调查
    verify involved job  刘鹏测试    auto_01     首次调查
    verify pending job  刘鹏测试2    auto_02     首次调查
    verify pending job  刘鹏测试3    auto_03     首次调查

    log     将auto_02调查通过
    commit to first verify   刘鹏测试2  auto_02
    log     验证auto_02分配到了一审，其他进件依然在首次调查节点
    verify pending job  刘鹏测试    auto_02     待一审
    verify done job  刘鹏测试2    auto_02     首次调查
    verify involved job  刘鹏测试2    auto_02     首次调查
    verify pending job  刘鹏测试    auto_01     待一审
    verify pending job  刘鹏测试3    auto_03     首次调查

    log     将auto_03调查通过
    commit to first verify   刘鹏测试3  auto_03
    log     验证auto_03分配到了一审，没有进件在首次调查节点
    verify pending job  刘鹏测试2    auto_03     待一审
    verify done job  刘鹏测试3    auto_03     首次调查
    verify involved job  刘鹏测试3    auto_03     首次调查
    verify pending job  刘鹏测试    auto_01     待一审
    verify pending job  刘鹏测试    auto_02     待一审

Test Flow Task By People For Second Verify
    log     设置首次调查的人员
    flow setup by people for inquireing   刘鹏测试  刘鹏测试2   刘鹏测试3

    log     设置一审的人员
    flow setup by people for inquire success  刘鹏测试  刘鹏测试2   刘鹏测试3

    log     设置二审的人员
    flow setup by people for first verify success  刘鹏测试2   刘鹏测试3

    log     分配首次调查的进件
    populate task by nick names  auto_01    auto_02    auto_03

    log     将auto_01调查通过
    commit to first verify   刘鹏测试  auto_01

    log     将auto_02调查通过
    commit to first verify   刘鹏测试2  auto_02

    log     将auto_03调查通过
    commit to first verify   刘鹏测试3  auto_03
