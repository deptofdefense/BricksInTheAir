# aerobot.py
# Created for defcon28 aerospace village

import threading    # needed for threading
import time         # needed for sleep
import binascii     # needed for serial
import yaml         # needed for config
import asyncio      # needed for async ops
import argparse

from twitchio.ext import commands           # from tutorial, for twitch
from BricksInTheAir import BricksInTheAir   # needed to manage game
from UserList import UserList               # needed for user management
from BrickUser import BrickUser             # needed for user management

from gameDisplay import DisplayManager  # needed for running the game overlay

CFG = None  # global CFG settings

with open("config.yml", "r") as ymlfile:
    creds = yaml.safe_load(ymlfile)

with open("script.yml", "r") as scriptfile:
    script = yaml.safe_load(scriptfile)

CFG = {**creds, **script}

# pulling the values from config.yml
# keeping them separate for flexibilitycode sharing
bot = commands.Bot(
    irc_token = CFG["twitch"]["TMI_TOKEN"],
    client_id = CFG["twitch"]["CLIENT_ID"],
    nick = CFG["twitch"]["BOT_NICK"],
    prefix = CFG["twitch"]["BOT_PREFIX"],
    initial_channels = CFG["twitch"]["CHANNEL"]
)

# manages the game
bia_game = BricksInTheAir(CFG)

# Display Manager to handle overlay
dispMan = DisplayManager(CFG)

# user list for managing active connections
userList = UserList(CFG, dispMan, bot)
userList.startUserThread()
dispMan.startDisplay()

# bot connection event
@bot.event
async def event_ready():

    global CFG, bia_game, userList, dispMan

    print(CFG["twitch"]["BOT_NICK"] + " is online!")
    ws = bot._ws
    await ws.send_privmsg(bot.initial_channels[0], f"/me is now operational")

# event for user entering something in chat
@bot.event
async def event_message(ctx):
    global CFG, bia_game, userList, dispMan

    if ctx.author.name.lower() == CFG["twitch"]["BOT_NICK"].lower():
        return
    await bot.handle_commands(ctx)
    print(f'{ctx.channel} - {ctx.author.name}: {ctx.content}')

# reset command - proof of concept
@bot.command(name='reset')
async def reset(ctx):
    global CFG, bia_game, userList, dispMan

    if ctx.author.name in CFG["admins"]:
        bia_game.reset(userList.getCurrentUser().getCurrentStep())
        await ctx.channel.send(f"{ctx.author.name} sent the command reset")
    else:
        await ctx.channel.send(f"{ctx.author.name}: nope")

# replay command - sets the current step to 0 so the user may replay the game
@bot.command(name='replay')
async def replay(ctx):
    global CFG, bia_game, userList, dispMan

    if userList.getCurrentUser().matchName(ctx.author.name):
        userList.getCurrentUser().resetTimeout()
        userList.getCurrentUser().setCurrentStep(0)
        bia_game.reset(userList.getCurrentUser().getCurrentStep())
        await ctx.channel.send(f"{ctx.author.name} sent the replay command")
    else:
        await ctx.channel.send(f"{ctx.author.name}, it is not your turn to use the ground station")

# generic command - meant to be flexible
@bot.command(name='cmd')
async def cmd(ctx):
    global CFG, bia_game, userList, dispMan

    if userList.getCurrentUser() != None:
        if userList.getCurrentUser().matchName(ctx.author.name):
            userList.getCurrentUser().resetTimeout()
            msg = bia_game.checkCmd(userList.getCurrentUser(), ctx.content[5:])
            dispMan.updateCmdMsg(ctx.content)
            userList.triggerChanges()
            await ctx.channel.send(f"{ctx.author.name} {msg}")
    else:
        await ctx.channel.send(f"{ctx.author.name}, it is not your turn.")

# join command - allows user to join the user list
@bot.command(name='join')
async def join(ctx):
    global CFG, bia_game, userList, dispMan

    if userList.addUser(ctx.author.name):
        if len(userList.getUserList()) == 1:
            bia_game.run_prolouge(userList.getCurrentUser())
            await ctx.channel.send(f"{ctx.author.name} has joined the user list for this challenge and is now the active user.")
            await ctx.channel.send(f"Question {userList.getCurrentUser().getCurrentStep()}: {userList.getCurrentUser().getQuestion()}")
        else:
            await ctx.channel.send(f"{ctx.author.name} has joined the user list.")
    else:
        await ctx.channel.send(f"{ctx.author.name}, you are already on the user list.")

# leave command - allows user to leave the user list before they timeout
@bot.command(name='leave')
async def leave(ctx):
    global CFG, bia_game, userList, dispMan

    print("leave cmd sent")
    if userList.removeUser(ctx.author.name):
        await ctx.channel.send(f"{ctx.author.name} has left the user list.")
    else:
        await ctx.channel.send(f"{ctx.author.name}, you are not on the user list.")

# help command - link to repo readme with instructions
@bot.command(name='help')
async def help(ctx):
    global CFG, bia_game, userList, dispMan

    await ctx.channel.send(f'Hello {ctx.author.name}: {CFG["text"]["help"]}')

@bot.command(name='hint')
async def hint(ctx):
    global CFG, bia_game, userList, dispMan

    if userList.getCurrentUser() != None:
        if userList.getCurrentUser().matchName(ctx.author.name):
            userList.getCurrentUser().resetTimeout()
            msg = userList.getCurrentUser().getHint()
            dispMan.updateCmdMsg(ctx.content)
            await ctx.channel.send(f"{ctx.author.name}: {msg}")
    else:
        await ctx.channel.send(f"{ctx.author.name}, it is not your turn to ask for a hint.")

@bot.command(name='goto')
async def goto(ctx):
    global CFG, bia_game, userList, dispMan

    if userList.getCurrentUser() != None:
        if userList.getCurrentUser().matchName(ctx.author.name):
            userList.getCurrentUser().resetTimeout()
            try:
                step = int(ctx.content[6:])
                msg = userList.getCurrentUser().setCurrentStep(step)
                bia_game.run_prolouge(userList.getCurrentUser())
                userList.triggerChanges()
                dispMan.updateCmdMsg(ctx.content)
            except ValueError:
                pass

            await ctx.channel.send(f"{ctx.author.name}: {msg}")
    else:
        await ctx.channel.send(f"{ctx.author.name}, it is not your turn to goto another step.")

@bot.command(name='question')
async def question(ctx):
    global CFG, bia_game, userList, dispMan

    if userList.getCurrentUser() != None:
        if userList.getCurrentUser().matchName(ctx.author.name):
            userList.getCurrentUser().resetTimeout()
            msg = userList.getCurrentUser().getQuestion()
            dispMan.updateCmdMsg(ctx.content)
            await ctx.channel.send(f"{ctx.author.name}: {msg}")
    else:
        await ctx.channel.send(f"{ctx.author.name}, it is not your turn to ask for a question.")



if __name__ == "__main__":
    bot.run()
