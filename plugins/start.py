import os
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
import time
from pyrogram import Client, filters
from pyrogram.types import ( InlineKeyboardButton, InlineKeyboardMarkup,ForceReply)
import humanize
from helper.database import  insert ,find_one
from pyrogram.file_id import FileId
CHANNEL = os.environ.get("CHANNEL", "")
import datetime

#Part of Day --------------------
currentTime = datetime.datetime.now()

if currentTime.hour < 12:
	wish = "Good morning."
elif 12 <= currentTime.hour < 18:
	wish = 'Good afternoon.'
else:
	wish = 'Good evening.'

#-------------------------------

@Client.on_message(filters.private & filters.command(["start"]))
async def start(client,message):
	insert(int(message.chat.id))
	await message.reply_text(text =f"""
	{wish} {message.from_user.mention}

	__𝙸 𝚊𝚖 𝚊 𝚏𝚒𝚕𝚎 𝚁𝚎𝚗𝚊𝚖𝚎𝚛 𝚋𝚘𝚝,
𝚂𝚎𝚗𝚝 𝚖𝚎 𝚊𝚗𝚢 𝙳𝚘𝚌𝚞𝚖𝚎𝚗𝚝 𝚘𝚛 𝚟𝚒𝚍𝚎𝚘 𝚊𝚗𝚍 𝚎𝚗𝚝𝚎𝚛 𝚗𝚎𝚠 𝚏𝚒𝚕𝚎𝚗𝚊𝚖𝚎 𝚝𝚘 𝚛𝚎𝚗𝚊𝚖𝚎 𝚒𝚝__
	""",reply_to_message_id = message.message_id ,  
	reply_markup=InlineKeyboardMarkup(
	 [[ InlineKeyboardButton("🍿 Update channel" ,url="https://t.me/MC_Moviescafe") ], 
	[InlineKeyboardButton("🎭 Movie Channel", url="https://t.me/MOVIE_CAFE_n1") ]  ]))



@Client.on_message(filters.private &( filters.document | filters.audio | filters.video ))
async def send_doc(client,message):
       update_channel = CHANNEL
       user_id = message.from_user.id
       if update_channel :
       	try:
       		await client.get_chat_member(update_channel, user_id)
       	except UserNotParticipant:
       		await message.reply_text("**__You are not subscribed my channel__** ",reply_to_message_id = message.message_id, reply_markup = InlineKeyboardMarkup([ [ InlineKeyboardButton("🍿 Update channel" ,url="https://t.me/MC_Moviescafe")]   ]))
       		return
       date = message.date
       _used_date = find_one(user_id)
       used_date = _used_date["date"]      
       c_time = time.time()
       LIMIT = 240
       then = used_date+ LIMIT
       left = round(then - c_time)
       conversion = datetime.timedelta(seconds=left)
       ltime = str(conversion)
       if left > 0:
       	await app.send_chat_action(message.chat.id, "typing")
       	await message.reply_text(f"```Sorry Dude I am not only for YOU \n Flood control is active so please wait for {ltime}```",reply_to_message_id = message.message_id)
       else:
       	
       	media = await client.get_messages(message.chat.id,message.message_id)
       	file = media.document or media.video or media.audio 
       	dcid = FileId.decode(file.file_id).dc_id
       	filename = file.file_name
       	filesize = humanize.naturalsize(file.file_size)
       	fileid = file.file_id
       	await message.reply_text(f"""__What do you want me to do with this file?__\n**File Name** :- {filename}\n**File Size** :- {filesize}\n**Dc ID** :- {dcid} """,reply_to_message_id = message.message_id,reply_markup = InlineKeyboardMarkup([[ InlineKeyboardButton("📝 Rename",callback_data = "rename"),InlineKeyboardButton("✖️ Cancel",callback_data = "cancel")  ]]))
