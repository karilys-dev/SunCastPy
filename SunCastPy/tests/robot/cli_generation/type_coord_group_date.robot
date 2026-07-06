*** Settings ***
Resource            ${CURDIR}/../resources/keywords.robot
Resource            ${CURDIR}/../resources/cli_generation_setup.robot
Variables           ${CURDIR}/../resources/variables.py

Suite Setup         Browser Setup    @{CLI_ARGS}
Suite Teardown      Browser Teardown


*** Variables ***
${OUTPUT_DIR}           NONE
${DAY_LIMIT}            3
@{CLI_ARGS}
...                     --group-by
...                     date
...                     --latitude
...                     18.441459
...                     --longitude
...                     -65.999504
...                     --limit=${DAY_LIMIT}
@{EXPECTED_FILES}
...                     ${DEFAULT_HTML_FILE}


*** Test Cases ***
Verify Report Creation
    Single Forecast Report    @{EXPECTED_FILES}    day_limit=${DAY_LIMIT}
