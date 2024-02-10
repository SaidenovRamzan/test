import json
import aiohttp
from aiogram.filters import CommandStart, Command
from aiogram.utils.markdown import hbold
from aiogram import Router, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder


router = Router()


@router.message(CommandStart())
async def command_start_handler(message: types.Message) -> None:
    await message.reply(f"Привет, {hbold(message.from_user.full_name)}!")
    await message.answer(f"Ваш Telegram ID: {hbold(message.chat.id)}")
    
                    
@router.message(Command('help'))
async def command_help_handler(message: types.Message) -> None:
    text = """Этот бот связывает ваши сообщения с сайта с чатом в боте и присылает уведомления"""
    await message.answer(f"{text}\n\n {message.text}")
   
   
