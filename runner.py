# I don't really comment on anything.
# Have fun reading this shit lol.
# Also, please thoroughly enjoy the mess.
import subprocess
import threading
import time
import re
import socketio
from flask import Flask, request, abort, jsonify
from colorama import init
import requests
from unicodedata import normalize
import psutil
import json
import os
from urllib.parse import unquote, quote_plus

init(convert=True)

default_config = """{
    "general":{
        "statusUpdate": "",
        "statusUpdateDelay": 5,
        "webhookURL": "",
        "runCommand": "./binmaster-slayer-linux",
        "bazaarUpdateTime": 120,
        "enableLogging": true,
        "hiddenUsername": false,
        "noOutputTimeout": 300
    },
    "security":{
        "whitelistedIPs": ["127.0.0.1"],
        "flaskPort": 8000,
        "socketIOPort": 1550,
        "password": "testing123"
    },
    "pings": {
        "pingID": 123456789,
        "pingOnMention": false,
        "pingOnAccuse": false,
        "pingOnFollow": false,
        "pingOnSpectating": false,
        "pingOnStaffCheck": false
    },
    "failsafe": {
        "OnMention": true,
        "OnAccuse": true,
        "OnFollow": false,
        "OnSpectating": false,
        "OnStaffCheck": false,
        "OnFollowTime": 60,
        "OnSpectateTime": 60
    }
}"""

if not os.path.isfile("bma_config.json"):
    print("[CONFIG] Config was not found.")
    with open("bma_config.json", "w+") as f:
        f.write(default_config)
    print("[CONFIG] A config file has been created.")

#vvv=====CONFIG=====vvv

global config
try:
    with open('bma_config.json', 'r') as f:
        
        config = json.load(f)
        #print("[config]", config)
except Exception as e:
    print("[config] error:", str(e))
    exit()

#vvv=====VARIABLES=====vvv

latestOutputLines = []
latestSocket_playerInfo = {'username': 'Unknown', 'healthInfo': '0/0', 'manaInfo': '0/0', 'location': 'Unknown'}
latestSocket_slayerInfo = {'questStart': 'Unknown', 'state': 'Unknown'}

latestFailsafeTriggers = []

startTime = int(time.time())

lastFailsafeTrigger = None
lastEyeTimestamp = None
lastRecievedMessage = None
totalEyes = 0
eyePrice = 0

errorMessages = ["client timed out after 30000 milliseconds", "Possible stall detected"]
isRunning = True
offlineSince = None

eyesPH = 0
coinsPH = 0

config_enableLogging = config['general']['enableLogging']
config_hiddenUsername = config['general']['hiddenUsername']
config_noOutputTimeout = config['general']['noOutputTimeout']

pingID = config['pings']['pingID']
ping_OnMention = config['pings']['pingOnMention']
ping_OnAccuse = config['pings']['pingOnAccuse']
ping_OnFollow = config['pings']['pingOnFollow']
ping_OnSpectating = config['pings']['pingOnSpectating']
ping_OnStaffCheck = config['pings']['pingOnStaffCheck']

failsafe_OnMention = config['failsafe']['OnStaffCheck']
failsafe_OnAccuse = config['failsafe']['OnAccuse']
failsafe_OnFollow = config['failsafe']['OnFollow']
failsafe_OnSpectating = config['failsafe']['OnSpectating']
failsafe_OnStaffCheck = config['failsafe']['OnStaffCheck']

failsafe_OnFollowTime = config['failsafe']['OnFollowTime']
failsafe_OnSpectateTime = config['failsafe']['OnSpectateTime']

#vvv=====FUNCTION=====vvv

def processFailsafeList():
    returnList = []
    for trigger in latestFailsafeTriggers:
        reason, time = trigger
        returnList.append({'name': '`⚠️` `Trigger Reason`','value': reason,'inline': True})
        returnList.append({'name': '`❓` `Resolved`','value': 'Yes','inline': True})
        returnList.append({'name': '`🚨` `Trigger Time`','value': f'<t:{time}:R>','inline': True})
    return returnList

def addFailsafe(message):
    global lastFailsafeTrigger
    lastFailsafeTrigger = getTime()
    if len(latestFailsafeTriggers) > 4:
        del latestFailsafeTriggers[0]
    latestFailsafeTriggers.append((message, getTime()))

def addLine(message):
    if len(latestOutputLines) > 50:
        del latestOutputLines[0]
    latestOutputLines.append(message)

def rmAnsi(text):
    ansi_escape = re.compile(r'\x1b\[[0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', text)

def sendWebhook(title, description, color):
    content = None
    if f"<@{pingID}>" in description:
        content = f"<@{pingID}>"
    params = {'wait': 'false'}
    timestampdesc = f"\n<t:{getTime()}:R>\n<t:{getTime()}>"
    json_data = {'content': content,'embeds': [{'title': str(title),'description': str(description+timestampdesc),'color': int(color),},],'attachments': []}
    requests.post(config['general']['webhookURL'],params=params,json=json_data,)

def getTime():
    return int(time.time())

def sanitizePlayer(player):
    player = player.split("Player ")[1].split(" has")[0]
    if " " in player:
        player = player.split(" ")[-1]
    player = normalize('NFKD', player).encode('ascii','ignore').decode().replace(" ", "")
    return player

def sanitizeTime(string):
    return float(string.split("for ")[1].split(" seconds")[0])

def killProcess(proc_pid):
    process = psutil.Process(proc_pid)
    for proc in process.children(recursive=True):
        proc.kill()
    process.kill()

def convertTime(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
     
    return "%d:%02d:%02d" % (hour, minutes, seconds)

#vvv=====SUBPROCESS=====vvv

def sendInput(process, input):
    process.stdin.write(input.encode() + b'\n')
    process.stdin.flush()
    time.sleep(0.2)

def processOutput(process, output):
    global lastFailsafeTrigger
    global latestFailsafeTriggers
    global noOutputTimeout
    print("[STDOUT]", output)
    noOutputTimeout = getTime()
    #processed_output = rmAnsi(output)
    addLine(output)
    if "Out of sync" in output:
        sendWebhook("Sync Detection", f"Out of Sync.", 16277083)
    for error in errorMessages:
        if error in output:
            outputPane = '\n'.join(latestOutputLines)
            sendWebhook("Error Handler", f"Error detected.\n\n```{outputPane}```", 15942467)
            try:
                killProcess(process.pid)
            except:
                pass
            try:
                process.kill()
            except:
                pass
            try:
                process.terminate()
            except:
                pass
            sendWebhook("Error Handler", f"Successfully restarted bot.", 2752256)

def readSubprocess(process):
    while True:
        output = process.stdout.readline().decode().strip()
        if output:
            threading.Thread(target=processOutput, args=(process, output)).start()
        if noOutputTimeout > config_noOutputTimeout:
            try:
                killProcess(process.pid)
            except:
                pass
            try:
                process.kill()
            except:
                pass
            try:
                process.terminate()
            except:
                pass
        time.sleep(0.03)

def sendUserInput(process):
    while True:
        user_input = input()
        sendInput(process, user_input)

#vvv=====FLASK=====vvv
app = Flask(__name__)

@app.before_request
def limit_remote_addr():
    password = request.args.get('password')
    
    if password != config['security']['password']:
        if request.remote_addr not in config['security']['whitelistedIPs']:
            return jsonify({"error":"Forbidden"})

@app.route('/webhook', methods=['POST'])
def webhook():
    global process

    global lastEyeTimestamp
    global totalEyes

    global lastFailsafeTrigger

    data = request.json
    print("[DATA]", data)
    webhookMessage = data['embeds'][0]['description']
    webhookColor = data['embeds'][0]['color']
    webhookTitle = data['embeds'][0]['title']

    # print("[webhookTitle]", webhookTitle)
    # print("[webhookMessage]", webhookMessage)

    if webhookTitle == "Rare Drop" and "Summoning Eye" in webhookMessage:
        lastEyeTimestamp = getTime()
        totalEyes += 1

    if "Mention Detected" in webhookTitle and failsafe_OnMention:
        detectedPlayer = sanitizePlayer(webhookMessage)
        lastFailsafeTrigger = getTime()
        latestFailsafeTriggers.append(("Mentioned", getTime()))
        sendInput(process, "pause")
        time.sleep(1)
        sendInput(process, f"chat /ignore add {detectedPlayer}")
        time.sleep(1)
        while True:
            sendInput(process, "chat /hub")
            time.sleep(1.5)
            if '"map":"Hub"' in "".join(latestOutputLines[-10:]) or 'Warping...' in "".join(latestOutputLines[-10:]) or 'Sending to server' in "".join(latestOutputLines[-10:]):
                print("[failsafe] hubbed")
                sendWebhook("Mention Handler", f"Successfully handled player {detectedPlayer}", 2752256)
                sendInput(process, "resume")
                break

    if "Macro Accusation Detected" in webhookTitle and failsafe_OnAccuse:
        detectedPlayer = sanitizePlayer(webhookMessage)
        lastFailsafeTrigger = getTime()
        latestFailsafeTriggers.append(("Accused", getTime()))
        sendInput(process, "pause")
        time.sleep(1)
        sendInput(process, f"chat /ignore add {detectedPlayer}")
        time.sleep(1)
        while True:
            sendInput(process, "chat /hub")
            time.sleep(5)
            if '"map":"Hub"' in "".join(latestOutputLines[-10:]) or 'Warping...' in "".join(latestOutputLines[-10:]) or 'Sending to server' in "".join(latestOutputLines[-10:]):
                print("[failsafe] hubbed")
                sendWebhook("Mention Handler", f"Successfully handled player {detectedPlayer}", 2752256)
                sendInput(process, "resume")
                break

    if "Player Following" in webhookTitle and failsafe_OnFollow:
        if sanitizeTime(webhookMessage) >= failsafe_OnFollowTime:
            detectedPlayer = sanitizePlayer(webhookMessage)
            lastFailsafeTrigger = getTime()
            latestFailsafeTriggers.append(("Following", getTime()))
            sendInput(process, "pause")
            time.sleep(1)
            sendInput(process, f"chat /ignore add {detectedPlayer}")
            time.sleep(1)
            while True:
                sendInput(process, "chat /hub")
                time.sleep(5)
                if '"map":"Hub"' in "".join(latestOutputLines[-10:]) or 'Warping...' in "".join(latestOutputLines[-10:]) or 'Sending to server' in "".join(latestOutputLines[-10:]):
                    print("[failsafe] hubbed")
                    sendWebhook("Mention Handler", f"Successfully handled player {detectedPlayer}", 2752256)
                    sendInput(process, "resume")
                    break

    if "Player Spectating" in webhookTitle and failsafe_OnSpectating:
        if sanitizeTime(webhookMessage) >= failsafe_OnSpectateTime:
            detectedPlayer = sanitizePlayer(webhookMessage)
            lastFailsafeTrigger = getTime()
            latestFailsafeTriggers.append(("Spectating", getTime()))
            sendInput(process, "pause")
            time.sleep(1)
            sendInput(process, f"chat /ignore add {detectedPlayer}")
            time.sleep(1)
            while True:
                sendInput(process, "chat /hub")
                time.sleep(5)
                if '"map":"Hub"' in "".join(latestOutputLines[-10:]) or 'Warping...' in "".join(latestOutputLines[-10:]) or 'Sending to server' in "".join(latestOutputLines[-10:]):
                    print("[failsafe] hubbed")
                    sendWebhook("Mention Handler", f"Successfully handled player {detectedPlayer}", 2752256)
                    sendInput(process, "resume")
                    break

    if "Staff Check" in webhookTitle and failsafe_OnStaffCheck:
        lastFailsafeTrigger = getTime()
        latestFailsafeTriggers.append(("Staff Check", getTime()))



    if "Mention Detected" in webhookTitle and ping_OnMention:
        webhookMessage += f"\n<@{pingID}>"

    if "Macro Accusation Detected" in webhookTitle and ping_OnAccuse:
        webhookMessage += f"\n<@{pingID}>"

    if "Player Following" in webhookTitle and ping_OnFollow:
        webhookMessage += f"\n<@{pingID}>"

    if "Player Spectating" in webhookTitle and ping_OnSpectating:
        webhookMessage += f"\n<@{pingID}>"

    if "Staff Check" in webhookTitle and ping_OnStaffCheck:
        webhookMessage += f"\n<@{pingID}>"

    lastOutput = rmAnsi("\n".join(latestOutputLines[-10:]))
    description = webhookMessage + f'\n\nstdout:```{lastOutput}```'
    sendWebhook(webhookTitle, description, webhookColor)
    #print("[FLASK]", webhookMessage)
    return "200"

@app.route('/getStatus')
def getStatus():
    status = {
        "success": True,
        "status": {
            "username": latestSocket_playerInfo['username'],
            "serverStatus": isRunning,
            "serverUptime": int(startTime),
            "totalEyes": totalEyes,
            "eyesPH": float(round(eyesPH, 2))
        }
    }
    return jsonify(status)

@app.route('/startProcess')
def startProcess():
    global isRunning
    if isRunning == True:
        return jsonify({"error":"Process is already running!"})
    
    global startTime
    global totalEyes
    global latestOutputLines
    latestOutputLines = []
    totalEyes = 0
    isRunning = True
    startTime = getTime()
    return jsonify({"success":True})

@app.route('/stopProcess')
def stopProcess():
    global isRunning
    global offlineSince
    if not isRunning:
        return jsonify({"error":"Process is already stopped!"})
    isRunning = False
    offlineSince = getTime()
    try:
        killProcess(process.pid)
    except:
        pass
    try:
        process.kill()
    except:
        pass
    try:
        process.terminate()
    except:
        pass
    return jsonify({"success":True})

@app.route('/restartProcess')
def restartProcess():
    if isRunning == False:
        return jsonify({"error":"Process is not running!"})
    try:
        killProcess(process.pid)
    except:
        pass
    try:
        process.kill()
    except:
        pass
    try:
        process.terminate()
    except:
        pass
    return jsonify({"success":True})

@app.route('/sendMessage')
def sendMessage():
    message = request.args.get('message')
    if isRunning:
        if message:
            message = unquote(message)
            sendInput(process, message)
            return jsonify({"success":True})
    if not isRunning:
        return jsonify({"error":"Process is not running"})

@app.route('/triggerFailsafe')
def triggerFailsafe():
    global lastFailsafeTrigger
    global latestFailsafeTriggers
    hubbed = False
    player = request.args.get('message')
    if isRunning:
        detectedPlayer = unquote(player)
        lastFailsafeTrigger = getTime()
        latestFailsafeTriggers.append(("Manual Entry", getTime()))
        sendInput(process, "pause")
        time.sleep(1)
        sendInput(process, f"chat /ignore add {detectedPlayer}")
        time.sleep(1)
        while True:
            sendInput(process, "chat /hub")
            time.sleep(1.5)
            if '"map":"Hub"' in "".join(latestOutputLines[-10:]) or 'Warping...' in "".join(latestOutputLines[-10:]) or 'Sending to server' in "".join(latestOutputLines[-10:]):
                print("[failsafe] hubbed")
                hubbed = True
                sendWebhook("Mention Handler", f"(Manual Entry)\nSuccessfully handled player {detectedPlayer}", 2752256)
                sendInput(process, "resume")
                break
        if hubbed:
            return jsonify({"success":True})                
    if not isRunning:
        return jsonify({"error":"Process is not running"})

@app.route('/configToggleLogging')
def configToggleLogging():
    global config_enableLogging
    config_enableLogging = not config_enableLogging
    return jsonify({"success":True, "enableLogging":config_enableLogging})

@app.route('/configToggleHiddenUsername')
def configToggleHiddenUsername():
    global config_hiddenUsername
    config_hiddenUsername = not config_hiddenUsername
    return jsonify({"success":True, "hiddenUsername":config_hiddenUsername})

def run_flask():
    app.run(host='0.0.0.0', port=config['security']['flaskPort'])

flask_thread = threading.Thread(target=run_flask)
flask_thread.daemon = True
flask_thread.start()

#vvv=====SOCKETIO=====vvv
sio = socketio.Client()
@sio.event
def connect():
    print('[SOCKET] Connection established!')

@sio.on('playerInfo')
def message(data):
    global latestSocket_playerInfo
    if config_hiddenUsername:
        data['username'] = "`Hidden`"
    latestSocket_playerInfo = data
    
    #print("[SOCKET]", data)

@sio.on('slayerInfo')
def message(data):
    global latestSocket_slayerInfo
    latestSocket_slayerInfo = data
    #print("[SOCKET]", data)

def run_socket():
    while True:
        try:
            while True:
                sio.connect(f"http://127.0.0.1:{config['security']['socketIOPort']}/")
                sio.wait()
                time.sleep(5)
        except Exception as e:
            print(f"[SOCKET] Error: {str(e)}")
            time.sleep(5)


socket_thread = threading.Thread(target=run_socket)
socket_thread.daemon = True
socket_thread.start()

#vvv=====STATWEBHOOK=====vvv

def updateWebhook():
    global startTime, totalEyes, eyesPH, coinsPH
    while True:
        if isRunning == True:
            try:
                loggingData = rmAnsi("\n".join(latestOutputLines[-10:]))

                if not lastFailsafeTrigger:
                    lastFailsafeTriggerMessage = "None"
                elif lastFailsafeTrigger:
                    lastFailsafeTriggerMessage = f'<t:{lastFailsafeTrigger}:R>'

                if not lastEyeTimestamp:
                    lastEyeTimestampMessage = "None"
                elif lastEyeTimestamp:
                    lastEyeTimestampMessage = f'<t:{lastEyeTimestamp}:R>'

                if not loggingData:
                    loggingDataMessage = "None"
                elif loggingData:
                    loggingDataMessage = f'```{loggingData}```'

                if config_enableLogging:
                    loggingEmbed = {
                            'description': f'```ansi\n\x1b[2;2m\x1b[1;2m📜 [\x1b[1;33mLogging \x1b[0m\x1b[1;37mInformation\x1b[0m]\x1b[0m\x1b[0m\n```\n{loggingDataMessage}',
                            'color': 0,
                        }
                elif not config_enableLogging:
                    loggingEmbed = {
                            'description': f'```ansi\n[1;2m📜 [[1;33mLogging [0m[1;31mDisabled[0m][0m\n```',
                            'color': 0,
                        }

                #print("[WEBHOOK] called")
                try:
                    if totalEyes != 0:
                        timeDifference = time.time()-startTime
                        eyesPH = round((totalEyes/timeDifference)*3600, 2)
                        #print("eyesph", eyesPH)
                    else:
                        eyesPH = 0
                except:
                    eyesPH = 0

                try:
                    if totalEyes != 0:
                        coinsPH = round(eyesPH*eyePrice, 2)
                        #print("coinsph", coinsPH)
                    else:
                        coinsPH = 0
                except:
                    coinsPH = 0

                params = {
                    'wait': 'false',
                }

                json_data = {
                    'content': None,
                    'embeds': [
                        {
                            'description': '## `📢` __`Status Update`__',
                            'color': 13092807,
                        },
                        {
                            'description': '```ansi\n\x1b[1;2m❓ [\x1b[1;32mGeneral \x1b[0m\x1b[1;34mInformation\x1b[0m]\n\x1b[0m```',
                            'color': 2525906,
                            'fields': [
                                {
                                    'name': '`👤` `Username`',
                                    'value': str(latestSocket_playerInfo['username']),
                                    'inline': True,
                                },
                                {
                                    'name': '`⌛` `Uptime`',
                                    'value': f'<t:{str(startTime)}:R>',
                                    'inline': True,
                                },
                                {
                                    'name': '`👁️` `Total Eyes`',
                                    'value': str(totalEyes),
                                    'inline': True,
                                },
                                {
                                    'name': '`📝` `Current Task`',
                                    'value': str(latestSocket_slayerInfo['state']),
                                    'inline': True,
                                },
                                {
                                    'name': '`📍` `Current Location`',
                                    'value': str(latestSocket_playerInfo['location']),
                                    'inline': True,
                                },
                            ],
                        },
                        {
                            'description': '```ansi\n\x1b[2;2m\x1b[1;2m💲 [\x1b[1;32mStatistical \x1b[0m\x1b[1;30mInformation\x1b[0m]\x1b[0m\x1b[0m\n```',
                            'color': 11532947,
                            'fields': [
                                {
                                    'name': '`👁️` `Total Eyes`',
                                    'value': str(totalEyes),
                                    'inline': True,
                                },
                                {
                                    'name': '`💰` `Total Coins`',
                                    'value': str(f"{(totalEyes*eyePrice):,}"),
                                    'inline': True,
                                },
                                {
                                    'name': '`⏲️` `Eyes/HR`',
                                    'value': str(round(eyesPH, 2)),
                                    'inline': True,
                                },
                                {
                                    'name': '`🪙` `Coins/HR`',
                                    'value': str(f"{int(coinsPH):,}"),
                                    'inline': True,
                                },
                            ],
                        },
                        {
                            'description': '```ansi\n\x1b[1;2m🛡️ [\x1b[1;31mFailsafe \x1b[0m\x1b[1;37mInformation\x1b[0m]\x1b[0m```\n```ansi\n\x1b[1;2m\x1b[1;31m🆕 > \x1b[4;31mLatest Triggers\x1b[0m\x1b[1;31m\n\x1b[0m\x1b[0m\n```',
                            'color': 16277083,
                            'fields': processFailsafeList(),
                        },
                        loggingEmbed,
                        {
                            'description': '```ansi\n\x1b[1;2m⌛ [\x1b[1;33mTimestamp \x1b[0m\x1b[1;31mInformation\x1b[0m]\x1b[0m```',
                            'color': 15523394,
                            'fields': [
                                {
                                    'name': '`🚨` `Last Failsafe Trigger`',
                                    'value': lastFailsafeTriggerMessage,
                                    'inline': True,
                                },
                                {
                                    'name': '`🔄` `Last Webhook Update`',
                                    'value': f'<t:{getTime()}:R>',
                                    'inline': True,
                                },
                                {
                                    'name': '`👁️` `Last Eye`',
                                    'value': lastEyeTimestampMessage,
                                },
                            ],
                            'footer': {
                                'text': '⊹ 𝗕𝗠𝗔𝗱𝗱𝗼𝗻𝘀',
                            },
                        },
                    ],
                    'attachments': [],
                }

                response = requests.patch(
                    url=config['general']['statusUpdate'],
                    params=params,
                    json=json_data,
                )
                if response.status_code != 200:
                    print("[WEBHOOK]", config['general']['statusUpdate'], response.status_code, response.text)
            except Exception as e:
                print("[WEBHOOK] ", str(e))
            time.sleep(config['general']['statusUpdateDelay'])
        elif isRunning == False:
            if config_hiddenUsername:
                latestSocket_playerInfo['username'] = "`Hidden`"
            params = {
                'wait': 'true',
            }

            json_data = {
                'content': None,
                'embeds': [
                    {
                        'description': '## `🔴` __`Process Offline`__\n ⠀',
                        'color': 16711680,
                        'fields': [
                            {
                                'name': '`👤` `Stored Username`',
                                'value': str(latestSocket_playerInfo['username']),
                                'inline': True,
                            },
                            {
                                'name': '`🔄` `Last Process Check`',
                                'value': f'<t:{str(getTime())}:R>',
                                'inline': True,
                            },
                            {
                                'name': '`🔴` `Offline Since`',
                                'value': f'<t:{str(offlineSince)}:R>',
                                'inline': True,
                            },
                        ],
                    },
                    {
                        'description': f'## `🕓` __`Last Session`__\n\n`Start:` <t:{startTime}:R>\n`End:` <t:{offlineSince}:R>',
                        'color': 6160158,
                        'fields': [
                            {
                                'name': '`⌛` `Uptime`',
                                'value': str(convertTime(offlineSince-startTime)),
                                'inline': True,
                            },
                            {
                                'name': '`💰` `Total Coins`',
                                'value': str(round(totalEyes*eyePrice,2)),
                                'inline': True,
                            },
                            {
                                'name': '`👁️` `Total Eyes`',
                                'value': str(totalEyes),
                                'inline': True,
                            },
                            {
                                'name': '`⏲️` `Eyes/HR`',
                                'value': str(round(eyesPH,2)),
                                'inline': True,
                            },
                            {
                                'name': '`🪙` `Coins/HR`',
                                'value': str(coinsPH),
                                'inline': True,
                            },
                        ],
                    },
                ],
                'attachments': [],
            }

            response = requests.patch(
                url=config['general']['statusUpdate'],
                params=params,
                json=json_data,
            )

            time.sleep(5)

webhook_thread = threading.Thread(target=updateWebhook)
webhook_thread.daemon = True
webhook_thread.start()

#vvv=====BAZAAR=====vvv

def updatePrice():
    global eyePrice
    while True:
        info = requests.get("https://api.hypixel.net/v2/skyblock/bazaar").json()
        eyePrice = int(info['products']['SUMMONING_EYE']['quick_status']['sellPrice'])
        time.sleep(config['general']['bazaarUpdateTime'])

price_thread = threading.Thread(target=updatePrice)
price_thread.daemon = True
price_thread.start()

#vvv=====RESTART=====vvv

while True:
    if isRunning == True:
        process = subprocess.Popen(config['general']['runCommand'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)

        isRunning = True

        output_thread = threading.Thread(target=readSubprocess, args=(process,))
        output_thread.daemon = True
        output_thread.start()

        input_thread = threading.Thread(target=sendUserInput, args=(process,))
        input_thread.daemon = True
        input_thread.start()

        process.wait()

    print("Process killed isRunning:", isRunning)
    time.sleep(5)
