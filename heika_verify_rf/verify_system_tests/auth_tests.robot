*** Settings ***
Test Setup       Open Browser To Login Page
Test Teardown    Close Browser
Resource    ../resources/resource.robot
Library     String
Library      ../VerifyLibrary.py   http://${SERVER}    ${ADMIN USER}

*** Test Cases ***
Administrator permission test
    Login With Valid Account    ${ADMIN USER}   ${ADMIN PASSWORD}

    :FOR    ${node}    IN    @{TREE NODE TITLES}
    \   Click TreeNode		${node}
    \   Page Title Visible   ${node}

    Click TreeTitle     ${TREE TITLE ONLY NODE}
    Page Title Visible  ${TREE TITLE ONLY NODE}

Investigator permission test
    log     ${VALID USER}
    log     &{DEPARTMENT NAME AND ID}[组织]
    log     &{ROLE NAME AND ROLE ID}[调查人员]
    ${response} =  UPDATE VERIFY USER ROLE     ${VALID USER}   &{DEPARTMENT NAME AND ID}[组织]   &{ROLE NAME AND ROLE ID}[调查人员]
    log     ${response}
    Login With Valid Account    ${VALID USER}   ${VALID PASSWORD}

    :FOR    ${node}    IN    @{INV TREE NODE TITLES}
    \   Click TreeNode		${node}
    \   Page Title Visible   ${node}

    :FOR    ${node}    IN    @{INV TREE NODE TITLES NOT VISIBLE}
    \   TreeNode Not Visble  ${node}
    TreeTitle Not Visble  ${TREE TITLE ONLY NODE}

Audit permission test
    UPDATE VERIFY USER ROLE     ${VALID USER}   &{DEPARTMENT NAME AND ID}[组织]   &{ROLE NAME AND ROLE ID}[审核人员]
    Login With Valid Account    ${VALID USER}   ${VALID PASSWORD}

    :FOR    ${node}    IN    @{AUDIT TREE NODE TITLES}
    \   Click TreeNode		${node}
    \   Page Title Visible   ${node}

    Click TreeTitle     ${TREE TITLE ONLY NODE}
    Page Title Visible  ${TREE TITLE ONLY NODE}

    :FOR    ${node}    IN    @{AUDIT TREE NODE TITLES NOT VISIBLE}
    \   TreeNode Not Visble  ${node}

Audit manager permission testj
    UPDATE VERIFY USER ROLE     ${VALID USER}   &{DEPARTMENT NAME AND ID}[组织]   &{ROLE NAME AND ROLE ID}[审核经理]
    Login With Valid Account    ${VALID USER}   ${VALID PASSWORD}

    :FOR    ${node}    IN    @{AUDIT MANAGER TREE NODE TITLES}
    \   Click TreeNode		${node}
    \   Page Title Visible   ${node}

    Click TreeTitle     ${TREE TITLE ONLY NODE}
    Page Title Visible  ${TREE TITLE ONLY NODE}

    :FOR    ${node}    IN    @{AUDIT MANAGER TREE NODE TITLES NOT VISIBLE}
    \   TreeNode Not Visble  ${node}
