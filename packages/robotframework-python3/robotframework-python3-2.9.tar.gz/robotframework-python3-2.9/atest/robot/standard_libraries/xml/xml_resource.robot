*** Settings ***
Resource         atest_resource.robot

*** Variables ***
${NO LXML}        XML library reverted to use standard ElementTree because lxml module is not installed.

*** Keywords ***
Make test non-critical if lxml not available
    Return From Keyword If    ${SUITE.metadata['lxml']}
    Check Log Message    ${ERRORS[0]}     ${NO LXML}    WARN
    Set Test Message    Test made non-critical because lxml was not available.
    Remove Tags    regression
