*** Settings ***
Resource    ${CURDIR}/keywords.robot
Resource    ${CURDIR}/cli_generation_browser.robot


*** Keywords ***
Browser Setup
    [Documentation]    Prepare the suite by running the initial command to create files at a temporary directory
    [Arguments]    @{cli_args}
    ${temp_dir}=    Generate Test Site    @{cli_args}
    Set Suite Variable    ${OUTPUT_DIR}    ${temp_dir}

Browser Teardown
    [Documentation]    Close down the browser test by taking a screenshot and removing generated files
    [Arguments]    ${page}=index.html
    Capture Full Page Snapshot    ${page}
    Cleanup Temp Dir    ${OUTPUT_DIR}
