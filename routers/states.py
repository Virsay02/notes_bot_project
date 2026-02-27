from aiogram.fsm.state import State,StatesGroup


class NameFile(StatesGroup):
    name_file = State()
    inner_file = State()
    other_file = State()
    edit_note_file = State()