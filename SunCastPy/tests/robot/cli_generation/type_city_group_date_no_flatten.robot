*** Settings ***
Resource            ${CURDIR}/../resources/keywords.robot
Resource            ${CURDIR}/../resources/cli_generation_setup.robot
Variables           ${CURDIR}/../resources/variables.py

Suite Setup         Browser Setup    @{CLI_ARGS}
Suite Teardown      Browser Teardown


*** Variables ***
${OUTPUT_DIR}           NONE

@{CLI_ARGS}
...                     --group-by
...                     date
...                     --city
...                     ${DEFAULT_CITY}
...                     --no-flatten

@{EXPECTED_FILES}
...                     ${DEFAULT_HTML_FILE}


*** Test Cases ***
Verify Report Creation
    Single Forecast Report    @{EXPECTED_FILES}
