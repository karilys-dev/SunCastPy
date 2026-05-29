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
...                     --city
...                     San Juan

@{EXPECTED_FILES}
...                     index.html


*** Test Cases ***
Verify Report Creation
    Single Forecast Report    @{EXPECTED_FILES}
