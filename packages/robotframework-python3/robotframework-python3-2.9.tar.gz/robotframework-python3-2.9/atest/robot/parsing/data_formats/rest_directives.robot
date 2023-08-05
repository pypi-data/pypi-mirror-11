*** Settings ***
Suite Setup     Check is docutils installed
Force Tags      regression  jybot  pybot
Resource        formats_resource.robot

*** Test Cases ***
One ReST using code-directive
    ${status}  ${msg} =  Run Keyword And Ignore Error  Run sample file and check tests  parsing${/}data_formats${/}rest_directives${/}sample.rst
    Run Keyword If  "${DOCUTILS INSTALLED}" == "YES" and "${status}" == "FAIL"  FAIL  ${msg}
    Run Keyword Unless  "${DOCUTILS INSTALLED}" == "YES"  Clear error should be given when docutils is not installed

*** Keywords ***
Clear Error Should Be Given When Docutils Is Not Installed
    Stderr Should Match    [ ERROR ] Parsing '*rest_directives?sample.rst' failed:
    ...  Using reStructuredText test data requires having 'docutils'
    ...  module version 0.9 or newer installed.${USAGE TIP}
