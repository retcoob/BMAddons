# Commands

## All Commmands
`/all` commands run a command on every server.

`/all start` - Starts every server.\
`/all stop` - Stops every server.\
`/all restart` - Restart every process. This does not reset your stats!\
`/all status` - Gives a general rundown of what is currently going on with your servers. Information includes: Server Status, Server Uptime, Total Eyes, and Eyes/HR.

## One Commands
`/one` commands run a command on one server.

Required:
 - server option - a selected server option is required to run this command

`/one start` - Starts a server.\
`/one stop` - Stops a server.\
`/one restart` - Restarts a server.\
`/one message` - Sends a message to the server. You can use this to send commands such as `chat`, `pause` or `resume`. Chat commands have to have the `chat` prefix to be sent.\
`/one triggerfailsafe` - Triggers the failsafe. If you would like to `/ignore` and switch lobbies due to a presence of a user, but they are not explicitly saying your username (YouTubers, friends, etc), you can use this command. 

## Config Commands
`/config` commands temporarily change the config. These will reset in the next startup of BMAddons.

Required:
 - server option - a selected server option is required to run this command

`/config togglelogging` - Toggles logging for the status webhook. This can be used to hide a username, or if the logging is too bulky, this can also be used.
`/config togglehiddenusername` - This hides your username from most instances of embeds/messages. Great for using in screenshots as the aesthetic of the embed remains the same.