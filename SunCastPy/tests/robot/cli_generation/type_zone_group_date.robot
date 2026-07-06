*** Settings ***
Resource            ${CURDIR}/../resources/keywords.robot
Resource            ${CURDIR}/../resources/cli_generation_setup.robot

Suite Setup         Browser Setup    @{CLI_ARGS}
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
    ...    ${DEFAULT_HTML_FILE}

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
        ${city_name}=    Remove String    ${button}    .html
        Page Should Contain    ${city_name}
        Verify Forecast HTML Content    html_file=${OUTPUT_DIR}/${button}    day_limit=1    city_name=${city_name}
    END

    Close Browser
