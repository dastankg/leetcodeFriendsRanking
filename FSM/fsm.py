from aiogram.fsm.context import FSMContext

from aiogram.fsm.state import State, StatesGroup


class FSMFillForm(StatesGroup):
    fill_name = State()
