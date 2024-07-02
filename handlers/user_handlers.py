from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from lexicon.lexicon import LEXICON
from models.base import conn
from FSM.fsm import FSMFillForm
from aiogram.fsm.state import default_state

router = Router()


@router.message(CommandStart(), StateFilter(default_state))
async def welcome(message: Message):
    await message.answer(LEXICON[message.text])
    await message.answer(text=str(message.from_user.id))
    cur = conn.cursor()

    cur.execute(f"SELECT * FROM users WHERE user_id={message.from_user.id}")

    if cur.rowcount == 0:
        await message.answer(
            text='Чтобы перейти к заполнению анкеты - '
                 'отправьте команду /fillform'
        )

        cur.close()
        conn.close()
    else:
        await message.answer(text='Good!')




@router.message(Command(commands='help'), StateFilter(default_state))
async def help(message: Message):
    await message.answer(LEXICON[message.text])


@router.message(Command(commands='fillform'), StateFilter(default_state))
async def fillform(message: Message, state: FSMContext):
    await message.answer(text='Пожалуйста, введите ваше имя')
    await state.set_state(FSMFillForm.fill_name)


@router.message(StateFilter(FSMFillForm.fill_name), F.text)
async def fill_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    tmp = await state.get_data()
    print(tmp)
    await state.clear()
