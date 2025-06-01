from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
    KeyboardButtonRequestUser,
    KeyboardButtonRequestChat
)
from pyrogram.enums import ChatType
import os
import asyncio

# Bot credentials from environment (or hardcode for testing)
API_ID = int(os.environ.get("API_ID", 12345))
API_HASH = os.environ.get("API_HASH", "your_api_hash")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "your_bot_token")

bot = Client("userinfo_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@bot.on_message(filters.command("start") & filters.private)
async def start_handler(client: Client, message: Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="User 👤",
                    request_user=KeyboardButtonRequestUser(
                        request_id=1,
                        user_is_bot=False
                    )
                )
            ],
            [
                KeyboardButton(
                    text="Super Group 👥",
                    request_chat=KeyboardButtonRequestChat(
                        request_id=2,
                        chat_is_channel=False,
                        chat_is_forum=False,
                        chat_has_username=True
                    )
                )
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await message.reply(
        "👋 Welcome! Choose an option below to share a user or a group.",
        reply_markup=keyboard
    )

@bot.on_message(filters.user_shared)
async def handle_user_shared(client: Client, message: Message):
    user_id = message.user_shared.user_id
    try:
        user = await client.get_users(user_id)
        name = user.first_name + (" " + user.last_name if user.last_name else "")
        username = f"@{user.username}" if user.username else "No username"
        photo = await client.download_media(user.photo.big_file_id) if user.photo else None

        text = (
            f"👤 <b>User Info</b>\n"
            f"<b>ID:</b> <code>{user.id}</code>\n"
            f"<b>Name:</b> {name}\n"
            f"<b>Username:</b> {username}"
        )

        if photo:
            await message.reply_photo(photo=photo, caption=text, parse_mode="html")
            os.remove(photo)
        else:
            await message.reply(text, parse_mode="html")
    except Exception as e:
        await message.reply(f"Failed to get user info.\nError: {e}")

@bot.on_message(filters.chat_shared)
async def handle_chat_shared(client: Client, message: Message):
    chat_id = message.chat_shared.chat_id
    try:
        chat = await client.get_chat(chat_id)
        name = chat.title or chat.first_name
        username = f"@{chat.username}" if chat.username else "No username"
        photo = await client.download_media(chat.photo.big_file_id) if chat.photo else None

        text = (
            f"💬 <b>Chat Info</b>\n"
            f"<b>ID:</b> <code>{chat.id}</code>\n"
            f"<b>Name:</b> {name}\n"
            f"<b>Username:</b> {username}"
        )

        if photo:
            await message.reply_photo(photo=photo, caption=text, parse_mode="html")
            os.remove(photo)
        else:
            await message.reply(text, parse_mode="html")
    except Exception as e:
        await message.reply(f"Failed to get chat info.\nError: {e}")

bot.run()
