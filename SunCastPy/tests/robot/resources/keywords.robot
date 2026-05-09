*** Settings ***
Library         Process
Library         OperatingSystem
Variables       ${CURDIR}/variables.py


*** Keywords ***
Generate Forecast Site
    [Arguments]    ${output_dir}

    ${result}=    Run Process
    ...    forecast
    ...    --group-by
    ...    date
    ...    --zone
    ...    ${ZONE}
    ...    --output
    ...    ${output_dir}
    ...    shell=False
    ...    stdout=STDOUT
    ...    stderr=STDERR

    Log To Console    \n========== STDOUT ==========
    Log To Console    ${result.stdout}

    Log To Console    \n========== STDERR ==========
    Log To Console    ${result.stderr}

    RETURN    ${result}
