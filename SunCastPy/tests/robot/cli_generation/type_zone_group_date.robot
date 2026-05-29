*** Settings ***
Resource            ${CURDIR}/../resources/keywords.robot

Suite Setup         Generate Test Site
Suite Teardown      Browser Teardown


*** Variables ***
${OUTPUT_DIR}           NONE

@{CLI_ARGS}
...                     --group-by
...                     date
...                     --zone
...                     ${ZONE}

@{EXPECTED_FILES}
...                     Bayamon.html
...                     Carolina.html
...                     Catano.html
...                     Guaynabo.html
...                     San Juan.html
...                     Toa Alta.html
...                     Toa Baja.html
...                     Trujillo Alto.html


*** Test Cases ***
Generated Files Exist
    [Documentation]     Confirm that the expected file was created
    Verify Expected Files Exist
    ...    ${OUTPUT_DIR}
    ...    @{EXPECTED_FILES}
    Verify Expected Files Exist
    ...    ${OUTPUT_DIR}
    ...    index.html

Generated Pages Are Not Empty
    [Documentation]    Generated Pages Are Not Empty
    Verify Pages Are Not Empty
    ...    ${OUTPUT_DIR}
    ...    @{EXPECTED_FILES}

Validate Generated Index
    [Documentation]    Verify that the landing page has buttons for each of the cities in the zone
    Open Generated Site

    Page Should Contain    Forecast
    FOR    ${button}    IN    @{EXPECTED_FILES}
        ${button_name}=    Remove String    ${button}    .html
        Page Should Contain    ${button_name}
    END

    Close Browser
