*** Settings ***
Suite Setup      Run Tests    ${EMPTY}    variables/shared_scope.robot
Force Tags       regression    pybot    jybot
Resource         atest_resource.robot

*** Test Cases ***
List can overwrite scalar
    Check Test Case    ${TESTNAME}

Scalar can overwrite list
    Check Test Case    ${TESTNAME}

Variables from file
    Check Test Case    ${TESTNAME}
