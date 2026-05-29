*** Settings ***
Resource            ${CURDIR}/../resources/keywords.robot

Suite Setup         Generate Test Site
Suite Teardown      Cleanup Temp Dir    ${OUTPUT_DIR}


*** Variables ***
${OUTPUT_DIR}           NONE

@{CLI_ARGS}
...                     --group-by
...                     date
...                     --zone
...                     ${ZONE}

@{EXPECTED_FILES}
...                     index.html
...                     Bayamon.html
...                     Carolina.html
...                     Catano.html
...                     Guaynabo.html
...                     San Juan.html
...                     Toa Alta.html
...                     Toa Baja.html
...                     Trujillo Alto.html

@{EXPECTED_BUTTONS}
...                     Hourly Forecast
...                     Marine Forecast


*** Test Cases ***
Generated Files Exist
    [Documentation]     Confirm that the expected file was created
    Verify Expected Files Exist
    ...    ${OUTPUT_DIR}
    ...    @{EXPECTED_FILES}

Generated Pages Are Not Empty
    [Documentation]    Generated Pages Are Not Empty
    Verify Pages Are Not Empty
    ...    ${OUTPUT_DIR}
    ...    @{EXPECTED_FILES}
