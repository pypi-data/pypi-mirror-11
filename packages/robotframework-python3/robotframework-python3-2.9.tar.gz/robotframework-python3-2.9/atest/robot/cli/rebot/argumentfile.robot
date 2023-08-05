*** Settings ***
Test Setup      Empty Output Directory
Suite Setup     Set Runners
Force Tags      regression  pybot  jybot
Resource        atest_resource.robot
Resource        rebot_cli_resource.robot

*** Test Cases ***
Argument File
    ${content} =    Catenate    SEPARATOR=\n
    ...    --name From_Arg File    -D= Leading space    -M${SPACE*5}No:Spaces
    ...    \# comment line    ${EMPTY}
    ...    --log=none    -r=none    -o myout.xml    --outputdir ${MYOUTDIR}
    ...    ${MYINPUT}
    Create File  ${MYOUTDIR}${/}a.txt  ${content}
    ${output} =  Run  ${REBOT} --log disable_me.html --argumentfile ${MYOUTDIR}${/}a.txt 2>&1
    Should Not Contain  ${output}  ERROR
    Directory Should Contain  ${MYOUTDIR}  a.txt  myout.xml
    Process Output  ${MYOUTDIR}${/}myout.xml
    Should Be Equal  ${SUITE.name}  From Arg File
    Should Be Equal  ${SUITE.doc}  ${SPACE}Leading space
    Should Be Equal  ${SUITE.metadata['No']}  Spaces
