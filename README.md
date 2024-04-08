## Welcome to BMAddons!

**This project took 1.5 days to code! With just over `1,000` lines of code!**\
Please consider dona- just kidding.\
I don't care.

**Don't feel like reading all this shit?**\
Me neither.\
Head to [releases](https://github.com/retcoob/BMAddons/releases/) for the pre-compiled versions.

## Issues/Questions
If you encounter an issue or have any questions, make a issue [here](https://github.com/retcoob/BMAddons/issues).\
I may or may not fix/respond to them. I'm tired and lazy.\
There's a reason why I didn't include my Discord here.\
If you know it, please don't DM me asking questions.\
Just make an [issue](https://github.com/retcoob/BMAddons/issues).

## FAQ
Q: Does this work on `Windows` or `Linux`?\
A: This works on both.

I haven't gotten any questions yet.

# Table of Contents
* [Features](#Features)
  *  [Runner Features](###runner-features)
  *  [Informational Features](###informational-features)
  *  [Config Features](#config-features)
  *  [Authentication Features](#authentication-features)
  *  [Ping Features](#ping-features)
  *  [Failsafe Features](#failsafe-features)
  *  [Controller Features](#controller-features)
  *  [Commands Overview](#commands-overview)
* [Self-Install](#Self-Install)
* [Self-Compile](#Self-Compile)
* [Usage](#Usage)
* [Configuration](#Configuration)

## Features

### Runner Features

- **Auto-restart:** Ensures continuous operation even in case of crashes.
- **Auto-restart on stall:** Detects and rectifies runner stalling automatically.
- **Auto-restart on client timeout:** Reconnects and resumes operation if communication is lost.
- **Out of Sync Detection:** Alerts you promptly if runner and game fall out of sync.
- **Automatic `/ignore` and `/hub`:** Shields from unwanted interactions/mentions/accusations.
- **Status Updates:** Periodic updates on runner's activity.
- **Hide Username Option:** Prioritize privacy with an option to conceal your username.

![320315587-5c30109a-aacd-4d0a-92c2-5fb7488990b7](https://github.com/retcoob/BMAddons/assets/166263898/aeea5bfc-e59a-421a-8d6f-3010ab52d0ea)\
![320315609-cc470c94-e9e4-48db-afb0-3665ea4812d0](https://github.com/retcoob/BMAddons/assets/166263898/440ca379-0392-4cc3-b124-57b79c9b0671)\
![320315671-61a9efff-118c-4cd4-aede-a15876243790](https://github.com/retcoob/BMAddons/assets/166263898/7064d10c-3dca-486f-bd84-7016fe0d19aa)\
![320315713-36c85ffa-2b89-487c-88bf-5b0c1e1693bb](https://github.com/retcoob/BMAddons/assets/166263898/46dec70d-9e6b-41f7-9358-78767043defa)


### Informational Features

- **Username Display:** Shows your in-game username.
- **Uptime Tracking:** Monitors the duration of runner operation.
- **Total Eyes Count:** Keeps track of collected "eyes".
- **Current Task Indicator:** Displays runner's ongoing action.
- **Current Location Coordinates (x,y,z):** In-game position information.
- **Total Coins (with Real-time Bazaar Price):** Estimates total coins' value based on current bazaar prices.
- **Eyes Per Hour & Coins Per Hour Calculation:** Evaluates average earnings.
- **Failsafe Information:** Detailed insight into last failsafe trigger.
- **Logging Information:** Records chat history and runner activity.
- **Last Eye & Last Webhook Update Timestamp:** Time of the most recent eye collection and webhook update.
- **Session Summary:** Provides performance stats upon runner stoppage.

![320315756-34380471-d4ee-4551-aeb3-e36060fd9fa6](https://github.com/retcoob/BMAddons/assets/166263898/f776522b-4672-4270-b8d5-966b4f1698f9)

### Config Features

- **Status Update Message URL:** Customizable status update messages.
- **Status Update Delay:** Set intervals between updates.
- **Webhook URL Configuration:** Sends actions along with a debug output.
- **Run Command Customization:** Define runner start command.
- **Bazaar Update Time Control:** Manage frequency of bazaar price updates.
- **Logging Toggle:** Enable/disable logging functionality.
- **Hide Username Toggle:** Control username visibility.

![320315802-5f6d3024-4fe8-4758-bf8d-9c51ce803291](https://github.com/retcoob/BMAddons/assets/166263898/c325b28c-0958-44db-8c4d-e91c5dde9111)

### Authentication Features

- **IP Authentication:** Secure access through whitelisted IPs.
- **Password Authentication:** Password-based access control.

![320315822-a4c73685-7667-4f95-8988-a9b362567849](https://github.com/retcoob/BMAddons/assets/166263898/2f4fea1c-7ea5-43ca-8f47-815c5dbc20cf)

### Ping Features

- **Customizable Pings:** Configure automated pings for various events:
  - Mentions
  - Accusations
  - Following
  - Spectating
  - Staff checks

![320315833-0bf74a54-437d-4e80-98c3-c51cf2f7ac22](https://github.com/retcoob/BMAddons/assets/166263898/df3e28b1-39e7-47b3-944b-5f2c72030fd1)

### Failsafe Features

- **Triggered Failsafe Actions:** Initiate failsafe actions based on events like mentions, accusations, etc.:
  - Mentions
  - Accusations
  - Following
  - Spectating
  - Staff checks
  - Exceeding follow/spectate durations

![320315838-8c6dc5eb-a625-4886-be83-73f8226b52df](https://github.com/retcoob/BMAddons/assets/166263898/10e5d5f1-7a2b-4e16-8e04-49a0e7ae1a90)

### Controller Features

- **Multi-server/Account Support:** Manage multiple runners and accounts simultaneously.
- **Multi-owner Support:** Grant access to multiple owners.
- **Guild Link:** Connect the runner to a specific guild ID.

![320315893-79dd30d9-b071-4d47-aeec-ca2e75a4a38d](https://github.com/retcoob/BMAddons/assets/166263898/af92c19f-63b6-435f-a3c8-02b3c194d315)

### Commands Overview

- **All Commands:**
  - `all start`: Starts all connected runners.
  - `all stop`: Stops all connected runners.
  - `all restart`: Restarts all connected runners.
  - `all status update`: Provides a quick overview of all runner statuses.

![320315914-5cf20d67-7636-4891-a2c1-9150e95d4f9c](https://github.com/retcoob/BMAddons/assets/166263898/e9ad34f8-1fd9-470f-9503-4fb7648317d7)\
![320316148-7e865a98-82c1-4e61-98d8-cdc2fe3ee8c6](https://github.com/retcoob/BMAddons/assets/166263898/16b7bba6-d83f-490e-b480-838a855e84ae)\
![320316087-1589069e-fded-45a4-a845-45e6c943e2c5](https://github.com/retcoob/BMAddons/assets/166263898/ae324d1c-3e51-4f8f-a250-9efaa82d7102)\
![320315982-9a3cb793-8a49-4fec-99fe-465cb060960d](https://github.com/retcoob/BMAddons/assets/166263898/197a245e-817d-49e0-80d2-959df3a1364b)


- **Individual Runner Commands:**
  - Start, stop, restart, trigger failsafe, send message.

![320316202-d0bd9e7e-c3b4-4c98-826f-71d442a94b6c](https://github.com/retcoob/BMAddons/assets/166263898/5b20fe59-dbc4-4392-b608-7af0afcb1b60)\
![320316211-8e09f3f7-9b62-435f-af7a-10971a359c4b](https://github.com/retcoob/BMAddons/assets/166263898/71d85e6c-5e9b-4f9e-a2d2-842094c46dee)\
![320316236-c3777cc2-9477-4620-94b8-c4eeb6f18a15](https://github.com/retcoob/BMAddons/assets/166263898/01a308a8-aeb3-48ea-b3da-65fa301b1502)

- **Configuration Commands:**
  - `toggle hidden username`: Show or hide username.
  - `toggle logging`: Enable or disable logging.

![320316253-08c1f0cd-c3e8-4353-bd17-a04001145f8e](https://github.com/retcoob/BMAddons/assets/166263898/62e49e2d-9705-450f-85d5-d4436dd142a1)

## Self-Install
1. Install python3/pip3
2. `pip3 install "discord.py" "python-socketio[client]" colorama requests psutil flask`
3. Run `python3 runner.py`
## Self-Compile
1. Download python3/pip3
2. `pip3 install "discord.py" "python-socketio[client]" colorama requests psutil flask nuitka`
3. `python3 -m nuitka --onefile runner.py`
4. Wait for compile
5. `chmod +x runner.bin`
6. `./runner.bin`\
Compiling may improve resource usage!
## Usage
1. Modify your `webpage_port` to whatever you have in your bma_config `socketIOPort`
2. Make sure the password on your `bma_config.json` is **NOT** the default.
3. Change the password to whatever you'd like and remember the password must reflect correctly on the controller's config as well for it to work. Failure to do this **WILL** cause errors.
4. Be sure to `ufw allow <port>`
5. `chmox +x runner.bin`
6. `./runner.bin`
## Configuration
If you run all accounts on VPS, run the controller on your (or one of your) VPS as well.\
If you run all accounts locally, run the controller locally.\
If you run some accounts locally and some accounts on VPS, run controller locally.
