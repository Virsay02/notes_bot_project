from aiogram import Router, F
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from routers.states import NameFile
from services import get_file_path

router = Router()


@router.message(Command('edit'))
async def cmd_edit(message:Message,state:FSMContext,command:CommandObject):
    data = await state.get_data()
    filename = data.get('file_n')

    if not filename:
        await message.answer("Вы не выбрали файл. Выберите файл для  изменения в нем заметок")
        return


    if not command.args:
        await message.answer("Введите число для того чтобы изменить заметку по этому числу. Пример: /edit 5")
        return

    user_input_args_number = command.args.strip()

    if not user_input_args_number.isdigit():
        await message.answer("❌ Ошибка, Комманда принимает только числа")
        return

    notes_number = int(user_input_args_number)

    file_path = get_file_path(message.from_user.id, filename)

    if not file_path.exists():
        await message.answer("В этом файле пока нет записей.")
        return

    full_text = file_path.read_text(encoding='utf-8')
    notes = full_text.split("\n\n")
    notes = [note.strip() for note in notes if note.strip()]

    if not (1 <= notes_number <= len(notes)):
        await message.answer(f"Такой заметки нет ❌ Всего заметок в файле {len(notes)}")
        return

    await state.update_data(edit_note_number = notes_number)
    await state.set_state(NameFile.edit_note_file)

    old_text_note = notes[notes_number - 1]
    await message.answer(text = f"Вы выбрали заметку №{notes_number}\n\n"
                                f"Текущий текст: {old_text_note}\n\n"
                                f"Отправьте новый текст:")


@router.message(F.text, NameFile.edit_note_file)
async def handle_cmd_edit(message: Message, state: FSMContext):
    await state.update_data(new_note = message.text )
    data = await state.get_data()
    filename = data.get('file_n')
    number_note = data.get('edit_note_number')
    new_note_text = message.text

    file_path = get_file_path(message.from_user.id,filename)
    full_text = file_path.read_text(encoding='utf-8')

    notes = full_text.split("\n\n")
    notes = [note.strip() for note in notes if note.strip()]

    notes[number_note - 1] = new_note_text

    final_text = "\n\n".join(notes)
    final_text += "\n\n"

    file_path.write_text(final_text,encoding='utf-8')

    await state.set_state(NameFile.inner_file)
    await message.answer(f"Заметка № {number_note} успешно изменена ✅ ")


@router.message(Command("delete"))
async def cmd_delete(message:Message,state:FSMContext,command:CommandObject):
    data = await state.get_data()
    filename = data.get("file_n")

    if not filename:
        await message.answer("Файл по такому названию не найден")
        return

    if not command.args:
        await message.answer("Введите число для того чтобы удалить заметку по этому числу. Пример: /delete 5")
        return

    user_input_args_number = command.args.strip()
    if not user_input_args_number.isdigit():
        await message.answer("Ошибка, Команда принимает только числа")
        return

    notes_number = int(user_input_args_number)
    file_path = get_file_path(message.from_user.id,filename)

    if not file_path.exists():
        await message.answer("В этом файле пока нет записей.")
        return

    full_text = file_path.read_text(encoding='utf-8')

    notes = full_text.split("\n\n")
    notes = [note.strip() for note in notes if note.strip()]

    if not (1 <= notes_number <= len(notes)):
        await message.answer(f"❌ В файле нет такой заметки по такому номеру\nВсего заметок в файле {len(notes)}")
        return

    notes.pop(notes_number - 1)

    final_text = "\n\n".join(notes)

    if final_text:
        final_text += "\n\n"

    file_path.write_text(final_text,encoding='utf-8')

    await message.answer(f"Заметка № {notes_number} успешно удалена ✅")
