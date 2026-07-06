*** Settings ***
Library         Process
Library         OperatingSystem
Library         ${CURDIR}/tempdir.py
Library         SeleniumLibrary
Variables       ${CURDIR}/variables.py
Library         String
Library         ${CURDIR}/../resources/HtmlKeywords.py


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

Generate Test Site
    [Documentation]    Create the temp dir and run cli with args
    [Arguments]    @{cli_args}
    ${temp_dir}=    Create Temp Dir

    Generate Forecast Site
    ...    ${temp_dir}
    ...    @{cli_args}

    RETURN    ${temp_dir}

Verify Forecast HTML Content
    [Documentation]    Open the html file and make sure that the forecast report tables are not empty and that the page has a title
    [Arguments]    ${html_file}    ${day_limit}=1    ${city_name}=San Juan

    ${page}=    Load Html    ${html_file}
    Page Title Should Be    ${page}    🌤 SunCast Forecast
    City Should Be    ${page}    ${city_name}
    Forecast Day Limit Should Be    ${page}    ${day_limit}
    Page Should Have Forecast    ${page}

Single Forecast Report
    [Documentation]    Run a set of tests when it expects a single page to be created
    [Arguments]    @{EXPECTED_FILES}    ${day_limit}=1

    Verify Expected Files Exist
    ...    ${OUTPUT_DIR}
    ...    @{EXPECTED_FILES}

    ${file_count}=    Count Files In Directory    ${OUTPUT_DIR}
    Should Be Equal As Integers    ${file_count}    1

    Verify Pages Are Not Empty
    ...    ${OUTPUT_DIR}
    ...    @{EXPECTED_FILES}

    Verify Forecast HTML Content    html_file=${OUTPUT_DIR}/${DEFAULT_HTML_FILE}    day_limit=${day_limit}
