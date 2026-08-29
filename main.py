import os
import asyncio

from dotenv import load_dotenv
from telethon import TelegramClient, events

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message


load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

CHATIDS = [
    6988840497,
]


CHANNELS = [
    "t.me/Somethingwithchannelname",
]

KEYWORDS = [
    "авария",
    "взрыв",
    "тревога",
    "отключение",
    'test',
]


# Telethon
client = TelegramClient(
    "parser_session",
    API_ID,
    API_HASH
)

# Bot
bot = Bot(BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start_command(message: Message):
    await message.answer(
        "👋 Привет!\n\n"
        "Бот работает.\n"
        f"Твой Chat ID: {message.chat.id}"
    )


@client.on(events.NewMessage(chats=CHANNELS))
async def new_message_handler(event):
    text = event.raw_text.lower()

    found_words = [
        word for word in KEYWORDS
        if word.lower() in text
    ]

    if not found_words:
        return

    channel = await event.get_chat()

    message_text = (
        "🚨 Найдено ключевое слово!\n\n"
        f"📢 Канал: {getattr(channel, 'title', 'Неизвестен')}\n"
        f"🔑 Слова: {', '.join(found_words)}\n\n"
        f"📝 Сообщение:\n{event.raw_text}"
    )

    for CHAT_ID in CHATIDS:
        await bot.send_message(
        chat_id=CHAT_ID,
        text=message_text
    )


async def main():
    await client.start()

    print("Парсер запущен...")
    print("Каналы:", CHANNELS)
    print("Ключевые слова:", KEYWORDS)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())