# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s bika.cement -t test_mix_types.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src bika.cement.testing.BIKA_CEMENT_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/bika/cement/tests/robot/test_mix_types.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a MixTypes
  Given a logged-in site administrator
    and an add MixTypes form
   When I type 'My MixTypes' into the title field
    and I submit the form
   Then a MixTypes with the title 'My MixTypes' has been created

Scenario: As a site administrator I can view a MixTypes
  Given a logged-in site administrator
    and a MixTypes 'My MixTypes'
   When I go to the MixTypes view
   Then I can see the MixTypes title 'My MixTypes'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add MixTypes form
  Go To  ${PLONE_URL}/++add++MixTypes

a MixTypes 'My MixTypes'
  Create content  type=MixTypes  id=my-mix_types  title=My MixTypes

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the MixTypes view
  Go To  ${PLONE_URL}/my-mix_types
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a MixTypes with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the MixTypes title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
