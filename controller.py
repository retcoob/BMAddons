import discord
import os
import typing
from discord import app_commands
import json
from discord.ext import commands
import discord.ext.commands
import requests
from discord.ext.commands import check, is_owner
from urllib.parse import quote_plus

import discord.ext

with open('bmcontrol_config.json', 'r') as f:
    config = json.load(f)

botToken = config['botToken']
ownerIDs = config['ownerIDs']
guildID = config['guildID']
serverList = config['servers']

guildObject = discord.Object(id=guildID)

global serverChoices
serverChoices = []
for index, client in enumerate(serverList):
    ip, name, password = client
    serverName = f"{name} ({ip})"
    serverChoices.append(app_commands.Choice(name=serverName, value=str(index)))

def serverRequest(server, request, password, message=None):
    if message:
        try:
            return requests.get(f"http://{server}/{request}?password={password}&message={message}", timeout=1).json()
        except:
            return False
    if not message:
        try:
            return requests.get(f"http://{server}/{request}?password={password}", timeout=1).json()
        except:
            return False

intents = discord.Intents.all()
client = discord.ext.commands.Bot(command_prefix="!", intents=intents)

@client.event
async def on_ready():
    client.tree.copy_global_to(guild=guildObject)
    await client.tree.sync(guild=guildObject)
    await client.change_presence(status=discord.Status.online, activity=discord.CustomActivity(name='Waiting for commands.'))
    print("We have logged in as {0.user}".format(client))

def checkOwner(interaction: discord.Interaction) -> bool:
    print(interaction.user.id, ownerIDs)
    return interaction.user.id in ownerIDs

all = app_commands.Group(name="all", description="All commands apply to all servers.")

async def on_tree_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    print(interaction, error)
    await interaction.response.send_message(embed=discord.Embed(description=f"## `❌` __`Unauthorized`__\n\nYou are unauthorized to use this commmand!\n\nCommand: /{interaction.command.parent.name} {interaction.command.name}", color=discord.Color.red()))

client.tree.on_error = on_tree_error

@all.command(name="status", description="List all process statuses.")
@app_commands.check(checkOwner)
async def status(interaction: discord.Interaction):
    await interaction.response.send_message("```ansi\n[1;2m[1;34mProcessing...[0m[0m\n```\n\nPlease wait, this may take a few seconds.")
    embedList = [discord.Embed(description="## `🌐` __`Process Statuses`__", color=discord.Color.green())]

    for server in serverList:
        serverIP, serverName, password = server
        response = serverRequest(serverIP, "getStatus", password)
        print("[debug]", response)
        if response:
            if 'success' in response:
                username = response['status']['username']
                serverStatus = response['status']['serverStatus']
                serverUptime = response['status']['serverUptime']
                totalEyes = response['status']['totalEyes']
                eyesPH = response['status']['eyesPH']

                if serverStatus:
                    embed = discord.Embed(color=discord.Color.green()).add_field(name="`👤` `Username`", value=username, inline=True).add_field(name="`📊` `Status`", value="`🟢` Online", inline=True).add_field(name="`⌛` `Uptime`", value=f"<t:{serverUptime}:R>", inline=True).add_field(name="`👁️` `Total Eyes`", value=str(totalEyes), inline=True).add_field(name="`⏲️` `Eyes/HR`", value=str(eyesPH), inline=True)
                    embedList.append(embed)
                elif not serverStatus:
                    embed = discord.Embed(color=discord.Color.red()).add_field(name="`👤` `Servername`", value=username, inline=True).add_field(name="`📊` `Status`", value="`🔴` Offline", inline=True)
                    embedList.append(embed)
            if 'error' in response:
                embed = discord.Embed(description=f"### `🔴` `Error`\n\nServer responded with:\n\n```{response['error']}```\n\n`Server Name:` `{serverName}`\n`Server IP:` `{serverIP}`",color=discord.Color.red())
                embedList.append(embed)
        if not response:
            embed = discord.Embed(description=f"### `🔴` `Error`\n\nServer failed to respond\n\n`Server Name:` `{serverName}`\n`Server IP:` `{serverIP}`",color=discord.Color.red())
            embedList.append(embed)
    await (await interaction.original_response()).edit(embeds=embedList, content="")

@all.command(name="start", description="Start all processes.")
@app_commands.check(checkOwner)
async def status(interaction: discord.Interaction):
    await interaction.response.send_message("```ansi\n[1;2m[1;34mProcessing...[0m[0m\n```\n\nPlease wait, this may take a few seconds.")
    embedList = [discord.Embed(description="## `🟢` __`Start All`__", color=discord.Color.green())]

    for server in serverList:
        serverIP, serverName, password = server
        response = serverRequest(serverIP, "startProcess", password)
        print("[debug]", response)
        if response:
            if 'success' in response:
                    embed = discord.Embed(color=discord.Color.green()).add_field(name="`👤` `Servername`", value=serverName, inline=True).add_field(name="`📊` `Status`", value="`🟢` Online", inline=True)
                    embedList.append(embed)
            if 'error' in response:
                embed = discord.Embed(description=f"### `🔴` `Error`\n\nServer responded with:\n\n```{response['error']}```\n\n`Server Name:` `{serverName}`\n`Server IP:` `{serverIP}`",color=discord.Color.red())
                embedList.append(embed)
        if not response:
            embed = discord.Embed(description=f"### `🔴` `Error`\n\nServer failed to respond\n\n`Server Name:` `{serverName}`\n`Server IP:` `{serverIP}`",color=discord.Color.red())
            embedList.append(embed)
    await (await interaction.original_response()).edit(embeds=embedList, content="")

@all.command(name="stop", description="Stop all processes.")
@app_commands.check(checkOwner)
async def status(interaction: discord.Interaction):
    await interaction.response.send_message("```ansi\n[1;2m[1;34mProcessing...[0m[0m\n```\n\nPlease wait, this may take a few seconds.")
    embedList = [discord.Embed(description="## `⛔` __`Stop All`__", color=discord.Color.green())]

    for server in serverList:
        serverIP, serverName, password = server
        response = serverRequest(serverIP, "stopProcess", password)
        print("[debug]", response)
        if response:
            if 'success' in response:
                    embed = discord.Embed(color=discord.Color.green()).add_field(name="`👤` `Stored Username`", value=serverName, inline=True).add_field(name="`📊` `Status`", value="`🔴` Offline", inline=True)
                    embedList.append(embed)
            if 'error' in response:
                embed = discord.Embed(description=f"### `🔴` `Error`\n\nServer responded with:\n\n```{response['error']}```\n\n`Server Name:` `{serverName}`\n`Server IP:` `{serverIP}`",color=discord.Color.red())
                embedList.append(embed)
        if not response:
            embed = discord.Embed(description=f"### `🔴` `Error`\n\nServer failed to respond\n\n`Server Name:` `{serverName}`\n`Server IP:` `{serverIP}`",color=discord.Color.red())
            embedList.append(embed)
    await (await interaction.original_response()).edit(embeds=embedList, content="")

@all.command(name="restart", description="Stop all processes.")
@app_commands.check(checkOwner)
async def status(interaction: discord.Interaction):
    await interaction.response.send_message("```ansi\n[1;2m[1;34mProcessing...[0m[0m\n```\n\nPlease wait, this may take a few seconds.")
    embedList = [discord.Embed(description="## `🔄` __`Restart All`__", color=discord.Color.green())]

    for server in serverList:
        serverIP, serverName, password = server
        response = serverRequest(serverIP, "restartProcess", password)
        print("[debug]", response)
        if response:
            if 'success' in response:
                    embed = discord.Embed(color=discord.Color.green()).add_field(name="`👤` `Servername`", value=serverName, inline=True).add_field(name="`📊` `Status`", value="`🟡` Restarting...", inline=True)
                    embedList.append(embed)
            if 'error' in response:
                embed = discord.Embed(description=f"### `🔴` `Error`\n\nServer responded with:\n\n```{response['error']}```\n\n`Server Name:` `{serverName}`\n`Server IP:` `{serverIP}`",color=discord.Color.red())
                embedList.append(embed)
        if not response:
            embed = discord.Embed(description=f"### `🔴` `Error`\n\nServer failed to respond\n\n`Server Name:` `{serverName}`\n`Server IP:` `{serverIP}`",color=discord.Color.red())
            embedList.append(embed)
    await (await interaction.original_response()).edit(embeds=embedList, content="")

client.tree.add_command(all, guild=guildObject)

one = app_commands.Group(name="one", description="One commands apply to only 1 server.")

@one.command(name="start", description="Start a server.")
@app_commands.check(checkOwner)
@app_commands.choices(server=serverChoices)
async def start(interaction: discord.Interaction, server: app_commands.Choice[str]):
    serverIP, username, password = serverList[int(server.value)]
    response = serverRequest(serverIP, "startProcess", password)
    print("[debug]", response)
    if response:
        if 'success' in response:
            await interaction.response.send_message(embed=discord.Embed(color=discord.Color.green(), description="### `✅` `Success!`\n\nProcess has successfully `started`."))
        if 'error' in response:
            await interaction.response.send_message(embed = discord.Embed(description=f"### `🔴` `Error`\n\nServer responded with:\n\n```{response['error']}```\n\n`Server Name:` `{serverName}`\n`Server IP:` `{serverIP}`",color=discord.Color.red()))
    if not response:
        await interaction.response.send_message(embed=discord.Embed(description=f"### `🔴` `Error`\n\nServer failed to respond\n\n`Server Name:` `{serverName}`\n`Server IP:` `{serverIP}`",color=discord.Color.red()))

@one.command(name="stop", description="Stop a server.")
@app_commands.check(checkOwner)
@app_commands.choices(server=serverChoices)
async def stop(interaction: discord.Interaction, server: app_commands.Choice[str]):
    serverIP, serverName, password = serverList[int(server.value)]
    response = serverRequest(serverIP, "stopProcess", password)
    print("response", response)
    if response:
        if 'success' in response:
            await interaction.response.send_message(embed=discord.Embed(color=discord.Color.green(), description="### `✅` `Success!`\n\nProcess has successfully `stopped`."))
        if 'error' in response:
            await interaction.response.send_message(embed = discord.Embed(description=f"### `🔴` `Error`\n\nServer responded with:\n\n```{response['error']}```\n\n`Server Name:` `{serverName}`\n`Server IP:` `{serverIP}`",color=discord.Color.red()))
    if not response:
        await interaction.response.send_message(embed=discord.Embed(description=f"### `🔴` `Error`\n\nServer failed to respond\n\n`Server Name:` `{serverName}`\n`Server IP:` `{serverIP}`",color=discord.Color.red()))

@one.command(name="restart", description="Restart a server. This does not reset statistics.")
@app_commands.check(checkOwner)
@app_commands.choices(server=serverChoices)
async def restart(interaction: discord.Interaction, server: app_commands.Choice[str]):
    serverIP, serverName, password = serverList[int(server.value)]
    response = serverRequest(serverIP, "restartProcess", password)
    if response:
        if 'success' in response:
            await interaction.response.send_message(embed=discord.Embed(color=discord.Color.green(), description="### `✅` `Success!`\n\nProcess has successfully `restarted`."))
        if 'error' in response:
            await interaction.response.send_message(embed = discord.Embed(description=f"### `🔴` `Error`\n\nServer responded with:\n\n```{response['error']}```\n\n`Server Name:` `{serverName}`\n`Server IP:` `{serverIP}`",color=discord.Color.red()))
    if not response:
        await interaction.response.send_message(embed=discord.Embed(description=f"### `🔴` `Error`\n\nServer failed to respond\n\n`Server Name:` `{serverName}`\n`Server IP:` `{serverIP}`",color=discord.Color.red()))

@one.command(name="message", description="Ask the server to send a message to the process.")
@app_commands.check(checkOwner)
@app_commands.choices(server=serverChoices)
async def message(interaction: discord.Interaction, server: app_commands.Choice[str], message: str):
    print("[message]", quote_plus(message))
    serverIP, serverName, password = serverList[int(server.value)]
    response = serverRequest(serverIP, "sendMessage", password, quote_plus(message))
    if response:
        if 'success' in response:
            await interaction.response.send_message(embed=discord.Embed(color=discord.Color.green(), description=f"### `✅` `Success!`\n\nProcess has successfully executed `{message}`."))
        if 'error' in response:
            await interaction.response.send_message(embed = discord.Embed(description=f"### `🔴` `Error`\n\nServer responded with:\n\n```{response['error']}```\n\n`Server Name:` `{serverName}`\n`Server IP:` `{serverIP}`",color=discord.Color.red()))
    if not response:
        await interaction.response.send_message(embed=discord.Embed(description=f"### `🔴` `Error`\n\nServer failed to respond\n\n`Server Name:` `{serverName}`\n`Server IP:` `{serverIP}`",color=discord.Color.red()))

@one.command(name="triggerfailsafe", description="Ask the server to execute triggerFailsafe.")
@app_commands.check(checkOwner)
@app_commands.choices(server=serverChoices)
async def triggerFailsafe(interaction: discord.Interaction, server: app_commands.Choice[str], player: str):
    serverIP, serverName, password = serverList[int(server.value)]
    response = serverRequest(serverIP, "triggerFailsafe", password, quote_plus(player))
    if response:
        if 'success' in response:
            await interaction.response.send_message(embed=discord.Embed(color=discord.Color.green(), description="### `✅` `Success!`\n\nProcess has successfully executed `triggerFailsafe`."))
        if 'error' in response:
            await interaction.response.send_message(embed = discord.Embed(description=f"### `🔴` `Error`\n\nServer responded with:\n\n```{response['error']}```\n\n`Server Name:` `{serverName}`\n`Server IP:` `{serverIP}`",color=discord.Color.red()))
    if not response:
        await interaction.response.send_message(embed=discord.Embed(description=f"### `🔴` `Error`\n\nServer failed to respond\n\n`Server Name:` `{serverName}`\n`Server IP:` `{serverIP}`",color=discord.Color.red()))

client.tree.add_command(one, guild=guildObject)

config = app_commands.Group(name="config", description="Config apply to only 1 server at a time.")

@config.command(name="togglelogging", description="Toggle Logging")
@app_commands.check(checkOwner)
@app_commands.choices(server=serverChoices)
async def triggerFailsafe(interaction: discord.Interaction, server: app_commands.Choice[str]):
    serverIP, serverName, password = serverList[int(server.value)]
    response = serverRequest(serverIP, "configToggleLogging", password)
    if response:
        if 'success' in response:
            await interaction.response.send_message(embed=discord.Embed(color=discord.Color.green(), description=f"### `✅` `Success!`\n\nProcess has successfully toggled `enableLogging` to `{response['enableLogging']}`."))
        if 'error' in response:
            await interaction.response.send_message(embed = discord.Embed(description=f"### `🔴` `Error`\n\nServer responded with:\n\n```{response['error']}```\n\n`Server Name:` `{serverName}`\n`Server IP:` `{serverIP}`",color=discord.Color.red()))
    if not response:
        await interaction.response.send_message(embed=discord.Embed(description=f"### `🔴` `Error`\n\nServer failed to respond\n\n`Server Name:` `{serverName}`\n`Server IP:` `{serverIP}`",color=discord.Color.red()))

@config.command(name="togglehiddenusername", description="Toggle Hidden Usernames.")
@app_commands.check(checkOwner)
@app_commands.choices(server=serverChoices)
async def toggleHiddenUsername(interaction: discord.Interaction, server: app_commands.Choice[str]):
    serverIP, serverName, password = serverList[int(server.value)]
    response = serverRequest(serverIP, "configToggleHiddenUsername", password)
    if response:
        if 'success' in response:
            await interaction.response.send_message(embed=discord.Embed(color=discord.Color.green(), description=f"### `✅` `Success!`\n\nProcess has successfully toggled `hiddenUsername` to `{response['hiddenUsername']}`."))
        if 'error' in response:
            await interaction.response.send_message(embed = discord.Embed(description=f"### `🔴` `Error`\n\nServer responded with:\n\n```{response['error']}```\n\n`Server Name:` `{serverName}`\n`Server IP:` `{serverIP}`",color=discord.Color.red()))
    if not response:
        await interaction.response.send_message(embed=discord.Embed(description=f"### `🔴` `Error`\n\nServer failed to respond\n\n`Server Name:` `{serverName}`\n`Server IP:` `{serverIP}`",color=discord.Color.red()))

client.tree.add_command(config, guild=guildObject)

client.run(botToken)