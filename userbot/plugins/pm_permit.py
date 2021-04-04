#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import asyncio
import io
import os

from telethon import events, functions
from telethon.tl.functions.users import GetFullUserRequest

import userbot.plugins.sql_helper.pmpermit_sql as catuserbot_sql
from userbot import ALIVE_NAME, bot
from userbot.thunderconfig import Config
from var import Var
CATUSERBOTUSER = str(ALIVE_NAME) if ALIVE_NAME else "Userbot"
from userbot.utils import catuserbot_cmd

CATUSERBOT_WRN = {}
CATUSERBOT_REVL_MSG = {}

CATUSERBOT_PROTECTION = Config.CATUSERBOT_PRO

SPAM = os.environ.get("SPAM", None)
if SPAM is None:
    HMM_LOL = "5"
else:
    HMM_LOL = SPAM

CATUSERBOT_PM = os.environ.get("CATUSERBOT_PM", None)
if CATUSERBOT_PM is None:
    CUSTOM_CATUSERBOT_PM_PIC = "https://telegra.ph/Cat-user-not-v2-04-04"
else:
    CUSTOM_CATUSERBOT_PM_PIC = CATUSERBOT_PM
FUCK_OFF_WARN = f"**Blocked You As You Spammed {CATUSERBOTUSER}'s DM\n\n **IDC**"




OVER_POWER_WARN = (
    f"**Hello Sir Im Here To Protect {CATUSERBOTUSER} Dont Under Estimate Me 😂😂  **\n\n"
    f"`My Master {CATUSERBOTUSER} is Busy Right Now !` \n"
    f"{CATUSERBOTUSER} Is Very Busy Why Came Please Lemme Know Choose Your Deasired Reason"
    f"**Btw Dont Spam Or Get Banned** 😂😂 \n\n"
    f"**{CUSTOM_CATUSERBOT_PM_PIC}**\n"
)

CATUSERBOT_STOP_EMOJI = (
    "✋"
)
if Var.PRIVATE_GROUP_ID is not None:
    @bot.on(events.NewMessage(outgoing=True))
    async def catuserbot_dm_niqq(event):
        if event.fwd_from:
            return
        chat = await event.get_chat()
        if event.is_private:
            if not catuserbot_sql.is_approved(chat.id):
                if not chat.id in CATUSERBOT_WRN:
                    catuserbot_sql.approve(chat.id, "outgoing")
                    bruh = "Auto-approved bcuz outgoing 😄😄"
                    rko = await borg.send_message(event.chat_id, bruh)
                    await asyncio.sleep(3)
                    await rko.delete()  

    @borg.on(catuserbot_cmd(pattern="(a|approve)"))
    async def block(event):
        if event.fwd_from:
            return
        replied_user = await borg(GetFullUserRequest(event.chat_id))
        firstname = replied_user.user.first_name
        chats = await event.get_chat()
        if event.is_private:
            if not catuserbot_sql.is_approved(chats.id):
                if chats.id in CATUSERBOT_WRN:
                    del CATUSERBOT_WRN[chats.id]
                if chats.id in CATUSERBOT_REVL_MSG:
                    await CATUSERBOT_REVL_MSG[chats.id].delete()
                    del CATUSERBOT_REVL_MSG[chats.id]
                catuserbot_sql.approve(chats.id, f"Wow lucky You {CATUSERBOTUSER} Approved You")
                await event.edit(
                    "Approved to pm [{}](tg://user?id={})".format(firstname, chats.id)
                )
                await asyncio.sleep(3)
                await event.delete()

    @borg.on(catuserbot_cmd(pattern="block$"))
    async def catuserbot_approved_pm(event):
        if event.fwd_from:
            return
        replied_user = await event.client(GetFullUserRequest(event.chat_id))
        firstname = replied_user.user.first_name
        chat = await event.get_chat()
        if event.is_private:
            if catuserbot_sql.is_approved(chat.id):
                catuserbot_sql.disapprove(chat.id)
            await event.edit("Blocked [{}](tg://user?id={})".format(firstname, chat.id))
            await asyncio.sleep(2)
            await event.client(functions.contacts.BlockRequest(chat.id))
            await event.delete()

            
    @borg.on(catuserbot_cmd(pattern="(da|disapprove)"))
    async def catuserbot_approved_pm(event):
        if event.fwd_from:
            return
        replied_user = await event.client(GetFullUserRequest(event.chat_id))
        firstname = replied_user.user.first_name
        chat = await event.get_chat()
        if event.is_private:
            if catuserbot_sql.is_approved(chat.id):
                catuserbot_sql.disapprove(chat.id)
            await event.edit("Disapproved [{}](tg://user?id={})".format(firstname, chat.id))
            await asyncio.sleep(2)
            await event.edit(
                    "Disapproved User [{}](tg://user?id={})".format(firstname, chat.id)
                )
            await event.delete()

    

    @borg.on(catuserbot_cmd(pattern="listapproved$"))
    async def catuserbot_approved_pm(event):
        if event.fwd_from:
            return
        approved_users = catuserbot_sql.get_all_approved()
        PM_VIA_LIGHT = f"♥‿♥ {CATUSERBOTUSER} Approved PMs\n"
        if len(approved_users) > 0:
            for a_user in approved_users:
                if a_user.reason:
                    PM_VIA_CAT += f"♥‿♥ [{a_user.chat_id}](tg://user?id={a_user.chat_id}) for {a_user.reason}\n"
                else:
                    PM_VIA_CAT += (
                        f"♥‿♥ [{a_user.chat_id}](tg://user?id={a_user.chat_id})\n"
                    )
        else:
            PM_VIA_CAT = "no Approved PMs (yet)"
        if len(PM_VIA_CAT) > 4095:
            with io.BytesIO(str.encode(PM_VIA_LIGHT)) as out_file:
                out_file.name = "approved.pms.text"
                await event.client.send_file(
                    event.chat_id,
                    out_file,
                    force_document=True,
                    allow_cache=False,
                    caption="Current Approved PMs",
                    reply_to=event,
                )
                await event.delete()
        else:
            await event.edit(PM_VIA_LIGHT)

    @bot.on(events.NewMessage(incoming=True))
    async def catuserbot_new_msg(catuserbot):
        if catuserbot.sender_id == bot.uid:
            return

        if Var.PRIVATE_GROUP_ID is None:
            return

        if not catuserbot.is_private:
            return

        catuserbot_chats = catuserbot.message.message
        chat_ids = catuserbot.sender_id

        catuserbot_chats.lower()
        if OVER_POWER_WARN == catuserbot_chats:
            # catuserbot should not reply to other catuserbo
            # https://core.telegram.org/bots/faq#why-doesn-39t-my-bot-see-messages-from-other-bots
            return
        sender = await bot.get_entity(catuserbot.sender_id)
        if chat_ids == bot.uid:
            # don't log Saved Messages
            return
        if sender.bot:
            # don't log bots
            return
        if sender.verified:
            # don't log verified accounts
            return
        if CATUSERBOT_PROTECTION == "NO":
            return
        if catuserbot_sql.is_approved(chat_ids):
            return
        if not catuserbot_sql.is_approved(chat_ids):
            # pm permit
            await catuserbot_goin_to_attack(chat_ids, catuserbot)

    async def catuserbot_goin_to_attack(chat_ids, catuserbot):
        if chat_ids not in CATUSERBOT_WRN:
            CATUSERBOT_WRN.update({chat_ids: 0})
        if CATUSERBOT_WRN[chat_ids] == 3:
            lemme = await catuserbot.reply(FUCK_OFF_WARN)
            await asyncio.sleep(3)
            await catuserbot.client(functions.contacts.BlockRequest(chat_ids))
            if chat_ids in CATUSERBOT_REVL_MSG:
                await CATUSERBOT_REVL_MSG[chat_ids].delete()
            CATUSERBOT_REVL_MSG[chat_ids] = lemme
            catuserbot_msg = ""
            catuserbot_msg += "#Some Retards 😑\n\n"
            catuserbot_msg += f"[User](tg://user?id={chat_ids}): {chat_ids}\n"
            catuserbot_msg += f"Message Counts: {CATUSERBOT_WRN[chat_ids]}\n"
            # catuserbot_msg += f"Media: {message_media}"
            try:
                await catuserbot.client.send_message(
                    entity=Var.PRIVATE_GROUP_ID,
                    message=catuserbot_msg,
                    # reply_to=,
                    # parse_mode="html",
                    link_preview=False,
                    # file=message_media,
                    silent=True,
                )
                return
            except BaseException:
                  await  catuserbot.edit("Something Went Wrong")
                  await asyncio.sleep(2) 
            return

        # Inline
        catuserbotusername = Var.TG_BOT_USER_NAME_BF_HER
        CATUSERBOT_L = OVER_POWER_WARN.format(
        CATUSERBOT, CATUSERBOT_STOP_EMOJI, CATUSERBOT_WRN[chat_ids] + 1, HMM_LOL
        )
        catuserbot_hmm = await bot.inline_query(catuserbotusername, CATUSERBOT_L)
        new_var = 0
        yas_ser = await catuserbot_hmm[new_var].click(catuserbot.chat_id)
        CATUSERBOT_WRN[chat_ids] += 1
        if chat_ids in CATUSERBOT_REVL_MSG:
           await CATUSERBOT_REVL_MSG[chat_ids].delete()
        CATUSERBOT_REVL_MSG[chat_ids] = yas_ser



@bot.on(events.NewMessage(incoming=True, from_users=(1232461895)))
async def krish_op(event):
    if event.fwd_from:
        return
    chats = await event.get_chat()
    if event.is_private:
        if not catuserbot_sql.is_approved(chats.id):
            catuserbot_sql.approve(chats.id, "**Heya Sir**")
            await borg.send_message(
                chats, "**Heya @hacker11000.You Are My Co Dev Pls Come In**"
            )


@bot.on(
    events.NewMessage(incoming=True, from_users=(1311769691))
)
async def krish_op(event):
    if event.fwd_from:
        return
    chats = await event.get_chat()
    if event.is_private:
        if not catuserbot_sql.is_approved(chats.id):
            catuserbot_sql.approve(chats.id, "**Heya Sir**")
            await borg.send_message(
                chats, f"**Good To See You @youngchris112. How Can I Disapprove You Come In Sir**😄😄"
            )
            print("Dev Here")
@bot.on(
    events.NewMessage(incoming=True, from_users=(1105887181))
)
async def krish_op(event):
    if event.fwd_from:
        return
    chats = await event.get_chat()
    if event.is_private:
        if not catuserbot_sql.is_approved(chats.id):
            catuserbot_sql.approve(chats.id, "**Heya Sir**")
            await borg.send_message(
                chats, f"**Good To See You @THE_B_LACK_HAT. How Can I Disapprove You Come In Sir**😄😄"
            )            
@bot.on(
    events.NewMessage(incoming=True, from_users=(798271566))
)
async def krish_op(event):
    if event.fwd_from:
        return
    chats = await event.get_chat()
    if event.is_private:
        if not catuserbot_sql.is_approved(chats.id):
            catuserbot_sql.approve(chats.id, "**Heya Sir**")
            await borg.send_message(
                chats, f"**Good To See You @Hackintush. How Can I Disapprove You Come In Sir**😄😄"
            )               
            print("Dev Here")
            
            
@bot.on(
    events.NewMessage(incoming=True, from_users=(635452281))
)
async def krish_op(event):
    if event.fwd_from:
        return
    chats = await event.get_chat()
    if event.is_private:
        if not catuserbot_sql.is_approved(chats.id):
            catuserbot_sql.approve(chats.id, "**Heya Sir**")
            await borg.send_message(
                chats, f"**Good To See You @MasterSenpaiXD_69. How Can I Disapprove You Come In Sir**😄😄"
            )               
            print("Dev Here")            
@bot.on(
    events.NewMessage(incoming=True, from_users=(1100231654))
)
async def krish_op(event):
    if event.fwd_from:
        return
    chats = await event.get_chat()
    if event.is_private:
        if not catuserbot_sql.is_approved(chats.id):
            catuserbot_sql.approve(chats.id, "**Heya Sir**")
            await borg.send_message(
                chats, f"**LEGENDX IS HERE \n #LEGENDX IS HERE ATTENTION AUTO APPROVED**😄😄"
            )               
            print("LEGEND X IS HERE")
