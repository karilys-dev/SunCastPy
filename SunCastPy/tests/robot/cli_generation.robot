*** Settings ***
Library             OperatingSystem
# Library    Browser
Library             resources/tempdir.py
Resource            resources/keywords.robot

Suite Setup         Generate Test Site
Suite Teardown      Cleanup Output Directory


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
    Verify Expected Files Exist
    ...    ${OUTPUT_DIR}
    ...    @{EXPECTED_FILES}

Generated Pages Are Not Empty
    Verify Pages Are Not Empty
    ...    ${OUTPUT_DIR}
    ...    @{EXPECTED_FILES}


*** Keywords ***
Generate Test Site
    ${temp_dir}=    Create Temp Dir

    Set Suite Variable    ${OUTPUT_DIR}    ${temp_dir}

    Generate Forecast Site
    ...    ${OUTPUT_DIR}
    ...    @{CLI_ARGS}

Cleanup Output Directory
    Cleanup Temp Dir    ${OUTPUT_DIR}
