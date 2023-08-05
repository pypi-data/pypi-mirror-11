*** Settings ***

Resource  keywords.robot

Suite Setup  Setup
Suite Teardown  Teardown


*** Test cases ***

Show how to activate the add-on
    Enable autologin as  Manager
    Go to  ${PLONE_URL}/prefs_install_products_form
    Page should contain element  id=ps.fonts.iconmagic
    Assign id to element
    ...  xpath=//*[@id='ps.fonts.iconmagic']/parent::*
    ...  addons-psfontsiconmagic
    Assign id to element
    ...  xpath=//*[@id='ps.fonts.iconmagic']/ancestor::form
    ...  addons-enabled

    Highlight  addons-psfontsiconmagic
    Capture and crop page screenshot
    ...  setup_select_add_on.png
    ...  id=addons-enabled
