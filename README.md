## Welcome to BMAddons!

**This project took 1.5 days to code! With just over `1,000` lines of code!**\
Please consider dona- just kidding.\
I don't care.

**Don't feel like reading all this shit?**\
Me neither.\
Head to [releases](https://github.com/iforgotallmypasswords/bmaddons/releases/tag/release-1.0) for the pre-compiled versions.

## Issues/Questions
If you encounter an issue or have any questions, make a issue [here](https://github.com/iforgotallmypasswords/bmaddons/issues).\
I may or may not fix/respond to them. I'm tired and lazy.\
There's a reason why I didn't include my Discord here.\
If you know it, please don't DM me asking questions.\
Just make an [issue](https://github.com/iforgotallmypasswords/bmaddons/issues).

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

![image](https://github.com/iforgotallmypasswords/bmaddons/assets/163951148/5c30109a-aacd-4d0a-92c2-5fb7488990b7)
![image](https://github.com/iforgotallmypasswords/bmaddons/assets/163951148/cc470c94-e9e4-48db-afb0-3665ea4812d0)
![image](https://github.com/iforgotallmypasswords/bmaddons/assets/163951148/61a9efff-118c-4cd4-aede-a15876243790)
![image](https://github.com/iforgotallmypasswords/bmaddons/assets/163951148/36c85ffa-2b89-487c-88bf-5b0c1e1693bb)

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

![image](https://github.com/iforgotallmypasswords/bmaddons/assets/163951148/34380471-d4ee-4551-aeb3-e36060fd9fa6)

### Config Features

- **Status Update Message URL:** Customizable status update messages.
- **Status Update Delay:** Set intervals between updates.
- **Webhook URL Configuration:** Sends actions along with a debug output.
- **Run Command Customization:** Define runner start command.
- **Bazaar Update Time Control:** Manage frequency of bazaar price updates.
- **Logging Toggle:** Enable/disable logging functionality.
- **Hide Username Toggle:** Control username visibility.

![image](https://github.com/iforgotallmypasswords/bmaddons/assets/163951148/5f6d3024-4fe8-4758-bf8d-9c51ce803291)

### Authentication Features

- **IP Authentication:** Secure access through whitelisted IPs.
- **Password Authentication:** Password-based access control.

![image](https://github.com/iforgotallmypasswords/bmaddons/assets/163951148/a4c73685-7667-4f95-8988-a9b362567849)

### Ping Features

- **Customizable Pings:** Configure automated pings for various events:
  - Mentions
  - Accusations
  - Following
  - Spectating
  - Staff checks

![image](https://github.com/iforgotallmypasswords/bmaddons/assets/163951148/0bf74a54-437d-4e80-98c3-c51cf2f7ac22)


### Failsafe Features

- **Triggered Failsafe Actions:** Initiate failsafe actions based on events like mentions, accusations, etc.:
  - Mentions
  - Accusations
  - Following
  - Spectating
  - Staff checks
  - Exceeding follow/spectate durations

![image](https://github.com/iforgotallmypasswords/bmaddons/assets/163951148/8c6dc5eb-a625-4886-be83-73f8226b52df)

### Controller Features

- **Multi-server/Account Support:** Manage multiple runners and accounts simultaneously.
- **Multi-owner Support:** Grant access to multiple owners.
- **Guild Link:** Connect the runner to a specific guild ID.

![image](https://github.com/iforgotallmypasswords/bmaddons/assets/163951148/79dd30d9-b071-4d47-aeec-ca2e75a4a38d)


### Commands Overview

- **All Commands:**
  - `all start`: Starts all connected runners.
  - `all stop`: Stops all connected runners.
  - `all restart`: Restarts all connected runners.
  - `all status update`: Provides a quick overview of all runner statuses.

![image](https://github.com/iforgotallmypasswords/bmaddons/assets/163951148/5cf20d67-7636-4891-a2c1-9150e95d4f9c)
![image](https://github.com/iforgotallmypasswords/bmaddons/assets/163951148/7e865a98-82c1-4e61-98d8-cdc2fe3ee8c6)
![image](https://github.com/iforgotallmypasswords/bmaddons/assets/163951148/1589069e-fded-45a4-a845-45e6c943e2c5)
![image](https://github.com/iforgotallmypasswords/bmaddons/assets/163951148/9a3cb793-8a49-4fec-99fe-465cb060960d)

- **Individual Runner Commands:**
  - Start, stop, restart, trigger failsafe, send message.

![image](https://github.com/iforgotallmypasswords/bmaddons/assets/163951148/d0bd9e7e-c3b4-4c98-826f-71d442a94b6c)
![image](https://github.com/iforgotallmypasswords/bmaddons/assets/163951148/8e09f3f7-9b62-435f-af7a-10971a359c4b)
![image](https://github.com/iforgotallmypasswords/bmaddons/assets/163951148/c3777cc2-9477-4620-94b8-c4eeb6f18a15)


- **Configuration Commands:**
  - `toggle hidden username`: Show or hide username.
  - `toggle logging`: Enable or disable logging.

![image](https://github.com/iforgotallmypasswords/bmaddons/assets/163951148/08c1f0cd-c3e8-4353-bd17-a04001145f8e)

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
