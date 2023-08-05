*** Settings ***

Resource  plone/app/robotframework/keywords.robot
Variables  plone/app/testing/interfaces.py

*** Variables ***

${PORT} =  55001
${ZOPE_URL} =  http://localhost:${PORT}
${PLONE_URL} =  ${ZOPE_URL}/plone
${BROWSER} =  Firefox

*** Keywords ***

Start Browser and Autologin as
    [arguments]  ${role}

    Open Test Browser
    Enable Autologin as  $role

Start Browser and Log In as Site Owner
    Open Test Browser
    Log In As Site Owner
    Click Link  link=Home

