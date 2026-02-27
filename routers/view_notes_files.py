from aiogram import Router,F
from aiogram.filters import CommandStart, Command,CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils import markdown

from services import get_file_path, get_user_dir

router = Router()




@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Привет, я бот заметок!")


    @router.message(Command("cancel"))
    @router.message(F.text.casefold() == "cancel")
    async def cmd_cancel(message: Message, state: FSMContext):
        current_state = await state.get_state()

        if not current_state:
            await message.answer("Отменять нечего, мы в главном меню")
            return

        await state.clear()

        await message.answer(
            "Действие отменено ✅\n"
            "Мы вернулись в начало. Можешь выбрать другую команду."
        )


@router.message(Command('view'))
async def cmd_view(message:Message,state:FSMContext):
    data = await state.get_data()
    filename = data.get("file_n")

    if not filename:
        await message.answer("Файл не выбран!\nВыберите файл чтоб просмотреть его заметки")
        return

    file_path = get_file_path(message.from_user.id,filename)

    if not file_path.exists():
        await message.answer("В это файле нет записей")
        return

    full_text_file = file_path.read_text(encoding='utf-8')

    notes = full_text_file.split("\n\n")
    notes = [note.strip() for note in notes if note.strip()]


    response_text = f"Заметки из файла **{filename}**\n\n"

    for idx, note in enumerate(notes,start = 1):
        response_text += f"{idx} {note}\n\n"

    await message.answer(response_text)

@router.message(Command('note'))
async def cmd_note(message:Message,state:FSMContext,command:CommandObject):
    data = await state.get_data()
    filename = data.get("file_n")

    if not filename:
        await message.answer("Файл не найден,Попробуйте снова")
        return

    if not command.args:
        await message.answer("Пожалуйста, укажите номер заметки. Пример: /note 3")
        return


    user_input_args_number = command.args.strip()
    if not user_input_args_number.isdigit():
        await message.answer("Номер заметки должен быть числом! Пример: /note 3")
        return

    note_number = int(user_input_args_number)

    file_path = get_file_path(message.from_user.id,filename)

    if not file_path.exists():
        await message.answer("В этом файле пока нет записей.")
        return


    full_text_file = file_path.read_text(encoding='utf-8')


    notes = full_text_file.split("\n\n")
    notes = [note.strip() for note in notes if note.strip()]

    if 1 <= note_number <= len(notes):
        current_note = notes[note_number - 1]

        await message.answer(f"📌 Заметка №{note_number}:\n\n{current_note}")
    else:
        await message.answer("❌ В файле нет такой заметки по такому номеру")


@router.message(Command("list"))
async def cmd_list(message:Message):
    user_id = message.from_user.id

    user_dir = get_user_dir(user_id)

    md_files = list(user_dir.glob("*.md"))

    if len(md_files) == 0:
        await message.answer("У тебя пока нет ни одного файла 📭\nСоздай первый через команду /new")
        return

    final_text_bold = markdown.hbold(
        "Твои файлы:\n\n")

    for i, file_path in enumerate(md_files,start = 1):
        final_text_bold += f"{i}.{file_path.stem}\n\n"

    await message.answer(final_text_bold)


