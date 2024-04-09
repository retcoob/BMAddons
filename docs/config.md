## General
`statusUpdate` - [sends status updates](https://github.com/retcoob/BMAddons/assets/166263898/46dec70d-9e6b-41f7-9358-78767043defa)\
`statusUpdateDelay` - how often to update status updates\
`webhookURL` - sends original/standard binmaster webhook\
`runCommand` - command used to run binmaster\
`bazaarUpdateTime` - how often to update bazaar time\
`enableLogging` - enable logging in the statusUpdate embeds (/config toggleenablelogging also works)\
`hiddenUsername` - hides username from embeds\
`noOutputTimeout` - amount of time before with no output from the console to send a restart command\
`restartMessages` - when detected, restart the bot

## Pings
`whitelistedIPs` - whitelisted ip addresses\
`flaskPort` - port to host the server on, use this port in the controller config\
`socketIOPort` - set this port to the one found in your binmaster config\
`password` - be sure to change your password. use this password in the controller config as well\
`pingID` - your discord ID to ping\
`pingOnMention` - self explanatory\
`pingOnAccuse` - self explanatory\
`pingOnFollow` - self explanatory\
`pingOnSpectating` - self explanatory\
`pingOnStaffCheck` - self explanatory

## Failsafe
`OnMention` - self explanatory\
`OnAccuse` - self explanatory\
`OnFollow` - self explanatory\
`OnSpectating` - self explanatory\
`OnStaffCheck`  - self explanatory

## aiRespond 
### This feature is currently undergoing testing. Use at your own risk.
`isEnabled` - self explanatory\
`apiKey` - get your api key from https://ai.google.dev/ (its free forever)\
`OnMention` - self explanatory\
`OnAccuse` - self explanatory\
`prompt` - this prompt will be used to make legit looking responses. please TEST YOUR PROMPT before placing it here\
`timeBeforePause` - time before pausing the bot to similate reading\
`timeBeforeResume` - time before resuming after sending a message\
`typingWPM` - how fast to type in WPM\
`maxResponses` - maximum responses\
`switchAfterRespond` - switch servers after maxResponses or chatTimeout\
`ignoreAfterRespond` - ignore user after responding\
`chatTimeout` - amount of time before declaring the chat as dead