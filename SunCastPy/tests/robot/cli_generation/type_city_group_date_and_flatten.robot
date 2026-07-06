*** Settings ***
Resource            ${CURDIR}/../resources/keywords.robot
Resource            ${CURDIR}/../resources/cli_generation_setup.robot
Variables           ${CURDIR}/../resources/variables.py
Library             ${CURDIR}/../resources/HtmlKeywords.py

Suite Teardown      Browser Teardown


*** Variables ***
${OUTPUT_DIR}               NONE

@{CLI_ARGS}
...                         --group-by
...                         date
...                         --city
...                         ${DEFAULT_CITY}
...                         --flatten

@{CLI_ARGS_NO_FLATTEN}
...                         --group-by
...                         date
...                         --city
...                         ${DEFAULT_CITY}
...                         --no-flatten

@{EXPECTED_FILES}
...                         ${DEFAULT_HTML_FILE}


*** Test Cases ***
Verify Report Creation With Flatten Parameter
    Log    message=Running command with flatten    level=INFO
    Browser Setup    @{CLI_ARGS}
    Single Forecast Report    @{EXPECTED_FILES}
    ${rows_flattened}=    Get Forecast Row Count    file=${OUTPUT_DIR}/${DEFAULT_HTML_FILE}
    Remove File    path=${OUTPUT_DIR}/${DEFAULT_HTML_FILE}

    Log    message=Running command with no-flatten    level=INFO
    Generate Forecast Site
    ...    ${OUTPUT_DIR}
    ...    @{CLI_ARGS_NO_FLATTEN}
    Single Forecast Report    ${OUTPUT_DIR}/${DEFAULT_HTML_FILE}
    ${rows_not_flattened}=    Get Forecast Row Count    file=${OUTPUT_DIR}/index.html
    Should Be True    ${rows_flattened} < ${rows_not_flattened}
