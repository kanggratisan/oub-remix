# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
# All Credits to https://t.me/azrim89 for timestamp.

""" Userbot module which contains afk-related commands """

from datetime import datetime
import time
from random import choice, randint

from telethon.events import StopPropagation
from telethon.tl.functions.account import UpdateProfileRequest

from userbot import (AFKREASON, COUNT_MSG, CMD_HELP, ISAFK, BOTLOG,
                     BOTLOG_CHATID, USERS, PM_AUTO_BAN, bot)
from userbot.events import register

# ========================= CONSTANTS ============================
AFKSTR = [
    "`I'm busy right now. Please talk in a bag and when I come back you can just give me the bag!`",
    "I'm away right now. If you need anything, leave a message after the beep:\n`beeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeep`!",
    "`You missed me, next time aim better.`",
    "`I'll be back in a few minutes and if I'm not...,\nwait longer.`",
    "`I'm not here right now, so I'm probably somewhere else.`",
    "`Roses are red,\nViolets are blue,\nLeave me a message,\nAnd I'll get back to you.`",
    "`Sometimes the best things in life are worth waiting for…\nI'll be right back.`",
    "`I'll be right back,\nbut if I'm not right back,\nI'll be back later.`",
    "`If you haven't figured it out already,\nI'm not here.`",
    "`Hello, welcome to my away message, how may I ignore you today?`",
    "`I'm away over 7 seas and 7 countries,\n7 waters and 7 continents,\n7 mountains and 7 hills,\n7 plains and 7 mounds,\n7 pools and 7 lakes,\n7 springs and 7 meadows,\n7 cities and 7 neighborhoods,\n7 blocks and 7 houses...\n\nWhere not even your messages can reach me!`",
    "`I'm away from the keyboard at the moment, but if you'll scream loud enough at your screen, I might just hear you.`",
    "`I went that way\n---->`",
    "`I went this way\n<----`",
    "`Please leave a message and make me feel even more important than I already am.`",
    "`I am not here so stop writing to me,\nor else you will find yourself with a screen full of your own messages.`",
    "`If I were here,\nI'd tell you where I am.\n\nBut I'm not,\nso ask me when I return...`",
    "`I am away!\nI don't know when I'll be back!\nHopefully a few minutes from now!`",
    "`I'm not available right now so please leave your name, number, and address and I will stalk you later.`",
    "`Sorry, I'm not here right now.\nFeel free to talk to my userbot as long as you like.\nI'll get back to you later.`",
    "`I bet you were expecting an away message!`",
    "`Life is so short, there are so many things to do...\nI'm away doing one of them..`",
    "`I am not here right now...\nbut if I was...\n\nwouldn't that be awesome?`",
]


global USER_AFK  # pylint:disable=E0602
global afk_time  # pylint:disable=E0602
global afk_start
global afk_end
USER_AFK = {}
afk_time = None
afk_start = {}

# =================================================================
@register(outgoing=True, pattern="^.afk(?: |$)(.*)", disable_errors=True)
async def set_afk(afk_e):
    """ For .afk command, allows you to inform people that you are afk when they message you """
    message = afk_e.text
    string = afk_e.pattern_match.group(1)
    global ISAFK
    global AFKREASON
    global USER_AFK  # pylint:disable=E0602
    global afk_time  # pylint:disable=E0602
    global afk_start
    global afk_end
    user = await bot.get_me()
    global reason
    USER_AFK = {}
    afk_time = None
    afk_end = {}
    start_1 = datetime.now()
    afk_start = start_1.replace(microsecond=0)
    if string:
        AFKREASON = string
        await afk_e.edit(f"**Going AFK!**\
        \nReason: `{string}`")
    else:
        await afk_e.edit("**Going AFK!**")
    if user.last_name:
        await afk_e.client(UpdateProfileRequest(first_name=user.first_name, last_name=user.last_name + " [ I AM OFFLINE :) ]"))
    else:
        await afk_e.client(UpdateProfileRequest(first_name=user.first_name, last_name=" [ I AM OFFLINE :) ]"))
    if BOTLOG:
        await afk_e.client.send_message(BOTLOG_CHATID, "#AFK\nYou went AFK!")
    ISAFK = True
    afk_time = datetime.now()  # pylint:disable=E0602
    raise StopPropagation


@register(outgoing=True)
async def type_afk_is_not_true(notafk):
    """ This sets your status as not afk automatically when you write something while being afk """
    global ISAFK
    global COUNT_MSG
    global USERS
    global AFKREASON
    global USER_AFK  # pylint:disable=E0602
    global afk_time  # pylint:disable=E0602
    global afk_start
    global afk_end
    user = await bot.get_me()
    last = user.last_name
    if last and last.endswith(" [ I AM OFFLINE :) ]"):
        last1 = last[:-12]
    else:
        last1 = ""
    back_alive = datetime.now()
    afk_end = back_alive.replace(microsecond=0)
    if ISAFK:
        ISAFK = False
        msg = await notafk.respond("**I'm no longer AFK.**")
        time.sleep(3)
        await msg.delete()
        await notafk.client(UpdateProfileRequest(first_name=user.first_name, last_name=last1))
        if BOTLOG:
            await notafk.client.send_message(
                BOTLOG_CHATID,
                "You've recieved " + str(COUNT_MSG) + " messages from " +
                str(len(USERS)) + " chats while you were away",
            )
            for i in USERS:
                if str(i).isnumeric():
                    name = await notafk.client.get_entity(i)
                    name0 = str(name.first_name)
                    await notafk.client.send_message(
                        BOTLOG_CHATID,
                        "[" + name0 + "](tg://user?id=" + str(i) + ")" +
                        " sent you " + "`" + str(USERS[i]) + " message(s)`",
                    )
                else:  # anon admin
                    await notafk.client.send_message(
                        BOTLOG_CHATID,
                        "Anonymous admin in `" + i + "` sent you " + "`" +
                        str(USERS[i]) + " message(s)`",
                    )
        COUNT_MSG = 0
        USERS = {}
        AFKREASON = None


@register(incoming=True, disable_edited=True)
async def mention_afk(mention):
    """This function takes care of notifying the people who mention you that you are AFK."""
    global COUNT_MSG
    global USERS
    global ISAFK
    global USER_AFK  # pylint:disable=E0602
    global afk_time  # pylint:disable=E0602
    global afk_start
    global afk_end
    back_alivee = datetime.now()
    afk_end = back_alivee.replace(microsecond=0)
    afk_since = "a while ago"
    if ISAFK and mention.message.mentioned:
        now = datetime.now()
        datime_since_afk = now - afk_time  # pylint:disable=E0602
        time = float(datime_since_afk.seconds)
        days = time // (24 * 3600)
        time %= 24 * 3600
        hours = time // 3600
        time %= 3600
        minutes = time // 60
        time %= 60
        seconds = time
        if days == 1:
            afk_since = "Yesterday"
        elif days > 1:
            if days > 6:
                date = now + \
                    datetime.timedelta(
                        days=-days, hours=-hours, minutes=-minutes)
                afk_since = date.strftime("%A, %Y %B %m, %H:%I")
            else:
                wday = now + datetime.timedelta(days=-days)
                afk_since = wday.strftime('%A')
        elif hours > 1:
            afk_since = f"`{int(hours)}h{int(minutes)}m` ago"
        elif minutes > 0:
            afk_since = f"`{int(minutes)}m{int(seconds)}s` ago"
        else:
            afk_since = f"`{int(seconds)}s` ago"

        is_bot = False
        if (sender := await mention.get_sender()):
            is_bot = sender.bot
            if is_bot: return  # ignore bot

        chat_obj = await mention.client.get_entity(mention.chat_id)
        chat_title = chat_obj.title

        if mention.sender_id not in USERS or chat_title not in USERS:
            if AFKREASON:
                await mention.reply(f"I'm AFK since {afk_since}.\
                        \nReason: `{AFKREASON}`")
            else:
                await mention.reply(str(choice(AFKSTR)))
            if mention.sender_id is not None:
                USERS.update({mention.sender_id: 1})
            else:
                USERS.update({chat_title: 1})
        else:
            if USERS[mention.sender_id] % randint(2, 4) == 0:
                if AFKREASON:
                    await mention.reply(f"I'm still AFK since {afk_since}.\
                            \nReason: `{AFKREASON}`")
                else:
                    await mention.reply(str(choice(AFKSTR)))
            if mention.sender_id is not None:
                USERS[mention.sender_id] += 1
            else:
                USERS[chat_title] += 1
        COUNT_MSG += 1

@register(incoming=True, disable_errors=True)
async def afk_on_pm(sender):
    """ Function which informs people that you are AFK in PM """
    global ISAFK
    global USERS
    global COUNT_MSG
    global COUNT_MSG
    global USERS
    global ISAFK
    global USER_AFK  # pylint:disable=E0602
    global afk_time  # pylint:disable=E0602
    global afk_start
    global afk_end
    user = await bot.get_me()
    back_alivee = datetime.now()
    afk_end = back_alivee.replace(microsecond=0)
    afk_since = "**a while ago**"
    if sender.is_private and sender.sender_id != 777000 and not (
            await sender.get_sender()).bot:
        if PM_AUTO_BAN:
            try:
                from userbot.modules.sql_helper.pm_permit_sql import is_approved
                apprv = is_approved(sender.sender_id)
            except AttributeError:
                apprv = True
        else:
            apprv = True
        if apprv and ISAFK:
            now = datetime.now()
            datime_since_afk = now - afk_time  # pylint:disable=E0602
            time = float(datime_since_afk.seconds)
            days = time // (24 * 3600)
            time = time % (24 * 3600)
            hours = time // 3600
            time %= 3600
            minutes = time // 60
            time %= 60
            seconds = time
            if days == 1:
                afk_since = "**yesterday**"
            elif days > 1:
                if days > 6:
                    date = now + \
                        datetime.timedelta(
                            days=-days, hours=-hours, minutes=-minutes)
                    afk_since = date.strftime("%A, %Y %B %m, %H:%I")
                else:
                    wday = now + datetime.timedelta(days=-days)
                    afk_since = wday.strftime('%A')
            elif hours > 1:
                afk_since = f"`{int(hours)}h {int(minutes)}m`"
            elif minutes > 0:
                afk_since = f"`{int(minutes)}m {int(seconds)}s`"
            else:
                afk_since = f"`{int(seconds)}s`"
            if sender.sender_id not in USERS:
                if AFKREASON:
                    await sender.reply(f"I'm AFK since {afk_since}.\
                        \nReason: `{AFKREASON}`")
                else:
                    await sender.reply(str(choice(AFKSTR)))
                USERS.update({sender.sender_id: 1})
                COUNT_MSG = COUNT_MSG + 1
            elif apprv and sender.sender_id in USERS:
                if USERS[sender.sender_id] % randint(2, 4) == 0:
                    if AFKREASON:
                        await sender.reply(f"I'm still AFK since {afk_since}.\
                            \nReason: `{AFKREASON}`")
                    else:
                        await sender.reply(str(choice(AFKSTR)))
                    USERS[sender.sender_id] = USERS[sender.sender_id] + 1
                    COUNT_MSG = COUNT_MSG + 1
                else:
                    USERS[sender.sender_id] = USERS[sender.sender_id] + 1
                    COUNT_MSG = COUNT_MSG + 1


CMD_HELP.update({
    "afk":
    "`.afk` [Optional Reason]\
\nUsage: Sets you as afk.\nReplies to anyone who tags/PM's \
you telling them that you are AFK(reason).\n\nSwitches off AFK when you type back anything, anywhere.\
"
})
