"""
Телеграм-бот: отправляет голосовые сообщения (главы книги) по кнопкам меню.

"""

import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

# ==== НАСТРОЙКИ ====

# Токен читается либо из переменной окружения BOT_TOKEN (используется на хостинге),
# либо из локального файла config.py (используется на своём компьютере).
# Так токен никогда не попадает в код, который вы публикуете на GitHub.
try:
    from config import BOT_TOKEN as _LOCAL_TOKEN
except ImportError:
    _LOCAL_TOKEN = None

BOT_TOKEN = os.environ.get("BOT_TOKEN", _LOCAL_TOKEN)

if not BOT_TOKEN:
    raise SystemExit(
        "Токен не найден! Скопируйте config.example.py в config.py "
        "и впишите туда токен от @BotFather."
    )


CHAPTERS = {
    "Глава 1": "AwACAgIAAxkBAAMHaqzt2pic237nR8lJLNb3LNTsqZAAAqFZAAIVJlBIqbYJfWzod_A9BA",
    "Глава 2": "AwACAgIAAxkBAAMOaqzubvTIhBTlspMZlFxRSSC757sAArRZAAIVJlBIP-cI3ZQXHNM9BA",
    "Глава 3": "AwACAgIAAxkBAAMQaqzuqY8opkUOktN_BBR1S4p1znIAAld_AAKbSaFJ6_I-DFzjSUA9BA",
    "Глава 4": "AwACAgIAAxkBAAMSaqzvNOX2r6lYf-f23aU0labV_cEAAm9_AAKbSaFJOd8LeH5uvfE9BA",
    "Глава 5": "AwACAgIAAxkBAAMUaqzvSM4Ycgla5YHNC5dkNaYxfEEAAnedAAI5tOFIj4bKMQYk5c09BA",
    "Глава 6": "AwACAgIAAxkBAAMUaqzvSM4Ycgla5YHNC5dkNaYxfEEAAnedAAI5tOFIj4bKMQYk5c09BA",
    "Глава 7": "AwACAgIAAxkBAAMYaqzvVUFs3hO1hDU2u9yO84U116UAApCdAAI5tOFIygfc8np_8Us9BA",
    "Глава 8": "AwACAgIAAxkBAAMYaqzvVUFs3hO1hDU2u9yO84U116UAApCdAAI5tOFIygfc8np_8Us9BA",
    "Глава 9": "AwACAgIAAxkBAAMcaqzvZpw6XIlpqTkZSO6szIh4NT8AAqidAAI5tOFIAl8Kmd76-rU9BA",
    "Глава 10": "AwACAgIAAxkBAAMeaqzvbPZOT1n6e_I2zC5DSTebws4AAr-dAAI5tOFIjqRXeMoVwGs9BA",
}

# КОД БОТА

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


def build_menu() -> InlineKeyboardMarkup:
    """Собирает кнопки со списком глав."""
    buttons = [
        [InlineKeyboardButton(text=title, callback_data=f"chapter:{title}")]
        for title in CHAPTERS
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


@dp.message(CommandStart())
async def cmd_start(message: Message):
    if not CHAPTERS:
        await message.answer(
            "Главы ещё не добавлены. Пришлите мне голосовое сообщение, "
            "чтобы получить его file_id и добавить в код бота."
        )
        return
    await message.answer("Выберите главу:", reply_markup=build_menu())


@dp.callback_query(F.data.startswith("chapter:"))
async def send_chapter(callback: CallbackQuery):
    title = callback.data.split("chapter:", 1)[1]
    file_id = CHAPTERS.get(title)
    if file_id:
        await callback.message.answer_voice(file_id, caption=title)
    else:
        await callback.message.answer("Не нашёл эту главу, проверьте настройки.")
    await callback.answer()  # убирает "часики" на кнопке


@dp.message(F.voice)
async def get_file_id(message: Message):
    """Помощник: пришлите сюда голосовое — бот покажет его file_id."""
    file_id = message.voice.file_id
    await message.answer(
        f"file_id этого голосового:\n<code>{file_id}</code>\n\n"
        "Скопируйте его в словарь CHAPTERS в коде бота.",
        parse_mode="HTML",
    )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
