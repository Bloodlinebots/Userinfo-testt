import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

app = Client("tginfo", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


@app.on_message(filters.command("start"))
async def start(client, message):
    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("👤 User", switch_inline_query_current_chat="user"),
                InlineKeyboardButton("🤖 Bot", switch_inline_query_current_chat="bot")
            ],
            [
                InlineKeyboardButton("📣 Channel", switch_inline_query_current_chat="channel"),
                InlineKeyboardButton("👥 Chat", switch_inline_query_current_chat="chat")
            ]
        ]
    )
    user = message.from_user
    await message.reply(
        f"👋 <b>Welcome!</b>\n\n"
        f"🧑‍💻 Name: {user.first_name or ''} {user.last_name or ''}\n"
        f"🆔 ID: <code>{user.id}</code>\n"
        f"🔗 Username: @{user.username if user.username else 'None'}",
        reply_markup=buttons
    )


@app.on_message(filters.forwarded & filters.private)
async def forwarded_info(client, message):
    fwd = message.forward_from or message.forward_sender_name or message.forward_from_chat
    if not fwd:
        await message.reply("Couldn't identify forwarded source.")
        return

    if message.forward_from:
        await message.reply(
            f"👤 <b>User Forwarded</b>\n"
            f"🧑‍💻 Name: {fwd.first_name or ''} {fwd.last_name or ''}\n"
            f"🔗 Username: @{fwd.username if fwd.username else 'None'}\n"
            f"🆔 ID: <code>{fwd.id}</code>"
        )
    elif message.forward_from_chat:
        chat_type = "Channel" if fwd.type == "channel" else "Group"
        await message.reply(
            f"💬 <b>{chat_type} Forwarded</b>\n"
            f"📛 Title: {fwd.title}\n"
            f"🆔 ID: <code>{fwd.id}</code>\n"
            f"🔗 Username: @{fwd.username if fwd.username else 'None'}"
        )
    elif message.forward_sender_name:
        await message.reply(
            f"👤 <b>Anonymous Forward</b>\n"
            f"📝 Sender Name: {message.forward_sender_name}"
        )


app.run()
