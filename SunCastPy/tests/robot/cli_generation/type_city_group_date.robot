*** Settings ***
Resource            ${CURDIR}/../resources/keywords.robot

Suite Setup         Generate Test Site
Suite Teardown      Browser Teardown


*** Variables ***
${OUTPUT_DIR}           NONE

@{CLI_ARGS}
...                     --group-by
...                     date
...                     --city
...                     San Juan

@{EXPECTED_FILES}
...                     index.html


*** Test Cases ***
Generated Files Exist
    [Documentation]     Confirm that the expected file was created
    Verify Expected Files Exist
    ...    ${OUTPUT_DIR}
    ...    @{EXPECTED_FILES}

Verify File Count Is Exactly One
    [Documentation]    Verify File Count Is Exactly One
    ${file_count}=    Count Files In Directory    ${OUTPUT_DIR}
    Should Be Equal As Integers    ${file_count}    1

Generated Pages Are Not Empty
    [Documentation]    Generated Pages Are Not Empty
    Verify Pages Are Not Empty
    ...    ${OUTPUT_DIR}
    ...    @{EXPECTED_FILES}
