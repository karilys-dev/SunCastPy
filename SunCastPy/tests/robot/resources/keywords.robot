*** Settings ***
Library         Process
Library         OperatingSystem
Variables       ${CURDIR}/variables.py


*** Keywords ***
Generate Forecast Site
    [Documentation]    Run the create forecast command line function with different inputs
    [Arguments]
    ...    ${output_dir}
    ...    @{cli_args}

    ${result}=    Run Process
    ...    forecast
    ...    @{cli_args}
    ...    --output
    ...    ${output_dir}
    ...    shell=False
    ...    stdout=STDOUT
    ...    stderr=STDERR

    Log To Console    \n========== STDOUT ==========
    Log To Console    ${result.stdout}

    Log To Console    \n========== STDERR ==========
    Log To Console    ${result.stderr}

    # RETURN    ${result}
    Should Be Equal As Integers    ${result.rc}    0

Verify Expected Files Exist
    [Documentation]    Iterate over a list of files and confirm exists
    [Arguments]
    ...    ${output_dir}
    ...    @{expected_files}

    FOR    ${file}    IN    @{expected_files}
        ${full_path}=    Join Path
        ...    ${output_dir}
        ...    ${file}

        File Should Exist    ${full_path}
    END

Verify Pages Are Not Empty
    [Documentation]    Verify that the files are not empty
    [Arguments]
    ...    ${output_dir}
    ...    @{expected_files}

    FOR    ${file}    IN    @{expected_files}
        ${full_path}=    Join Path
        ...    ${output_dir}
        ...    ${file}

        ${content}=    Get File    ${full_path}

        Should Not Be Empty    ${content}

        Should Not Contain    ${content}    Traceback
        Should Not Contain    ${content}    undefined
        Should Not Contain    ${content}    None
    END
