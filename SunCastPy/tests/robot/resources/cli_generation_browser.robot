*** Settings ***
Resource        ${CURDIR}/keywords.robot
Variables       ${CURDIR}/../resources/variables.py


*** Keywords ***
Open Generated Site
    [Documentation]    Use selenium to open the webpages and run tests
    [Arguments]    ${page}=${DEFAULT_HTML_FILE}    ${output_dir}=${OUTPUT_DIR}
    ${options}=    Evaluate
    ...    sys.modules['selenium.webdriver'].ChromeOptions()
    ...    sys, selenium.webdriver

    ${service}=    Evaluate
    ...    sys.modules['selenium.webdriver.chrome.service'].Service(executable_path=r"/usr/bin/chromedriver")
    ...    sys, selenium.webdriver.chrome.service

    ${headless}=    Set Variable    --headless=new
    ${nosandbox}=    Set Variable    --no-sandbox
    ${disable}=    Set Variable    --disable-dev-shm-usage

    Call Method    ${options}    add_argument    ${headless}
    Call Method    ${options}    add_argument    ${nosandbox}
    Call Method    ${options}    add_argument    ${disable}

    Create Webdriver
    ...    Chrome
    ...    options=${options}
    ...    service=${service}

    Go To    file://${output_dir}/${page}

Capture Full Page Snapshot
    [Documentation]     Take a screenshot of the index.html to include in the report
    [Tags]    image
    [Arguments]    ${page}=${DEFAULT_HTML_FILE}
    Open Generated Site    ${page}

    Set Window Size    1600    5000

    ${safe_name}=    Replace String    ${SUITE NAME}    ${SPACE}    _

    Capture Page Screenshot    ./screenshots/${safe_name}.png

    Close Browser
