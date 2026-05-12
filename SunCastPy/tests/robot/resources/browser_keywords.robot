*** Settings ***
Library     OperatingSystem
Library     Browser
Library     ${CURDIR}/tempdir.py
Resource    ${CURDIR}/keywords.robot


*** Test Cases ***
Expected Buttons Exist
    Open Generated Homepage

    FOR    ${button}    IN    @{EXPECTED_BUTTONS}
        Get Element    text=${button}
    END

    Take Site Screenshot



*** Keywords ***
Open Generated Homepage
    ${index_file}=    Join Path
    ...    ${OUTPUT_DIR}
    ...    index.html

    New Browser    chromium    headless=True

    New Page    file://${index_file}

Take Site Screenshot
    Create Directory    ${EXECDIR}/screenshots

    ${screenshot}=    Join Path
    ...    ${EXECDIR}
    ...    screenshots
    ...    homepage.png

    Take Screenshot    path=${screenshot}
