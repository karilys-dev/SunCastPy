*** Settings ***
Library             OperatingSystem
Library             resources/tempdir.py
Resource            resources/keywords.robot
Variables           resources/variables.py

Suite Setup         Create Output Directory
Suite Teardown      Cleanup Output Directory


*** Variables ***
${OUTPUT_DIR}       NONE


*** Test Cases ***
CLI Generates Index HTML
    ${result}=    Generate Forecast Site    ${OUTPUT_DIR}

    Should Be Equal As Integers    ${result.rc}    0

    ${index_file}=    Join Path
    ...    ${OUTPUT_DIR}
    ...    ${OUTPUT_FILENAME}

    File Should Exist    ${index_file}


*** Keywords ***
Create Output Directory
    ${temp_dir}=    Create Temp Dir
    Set Suite Variable    ${OUTPUT_DIR}    ${temp_dir}

Cleanup Output Directory
    Cleanup Temp Dir    ${OUTPUT_DIR}
