from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from lexicon.lexicon import LEXICON

router = Router()


@router.message(CommandStart())
async def welcome(message: Message):
    await message.answer(LEXICON[message.text])


@router.message(Command(commands='help'))
async def help(message: Message):
    await message.answer(LEXICON[message.text])
