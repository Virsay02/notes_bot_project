
from aiogram import F,Router
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile

from services import get_file_path

from routers.states import NameFile

router = Router()



@router.message(Command("new"))
async def cmd_new(message: Message, state: FSMContext):
    await state.set_state(NameFile.name_file)
    await message.answer("Напишите имя файла:")


@router.message(F.text, NameFile.name_file)
async def handle_state_name_file(message: Message, state: FSMContext):
    filename = message.text.strip()
    if not filename:
        await message.answer("Файл не выбран,Повторите снова")
        return

    await state.update_data(file_n=filename)
    await state.set_state(NameFile.inner_file)

    await message.answer("Файл Создан ✅ Пишите заметки ✍️")

@router.message(Command("sendfile"),NameFile.inner_file)
async def cmd_sendfile(message:Message,state:FSMContext):
    data = await state.get_data()
    filename = data.get("file_n")

    if not filename:
        await message.answer("Нет файла")
        return

    file_path = get_file_path(message.from_user.id,filename)

    if not file_path.exists():

        await message.answer("❌ Файл не найден")
        return

    document = FSInputFile(file_path,f"{filename}.md")

    await message.reply_document(document,caption=f"Держи свой файл: {filename} 📂\n\nМожешь просто отправить следующий текст, и я допишу его туда же!")


@router.message(Command("change"))
async def change_file(message: Message, state: FSMContext):
    await state.set_state(NameFile.other_file)
    await message.answer("Введите название файла на который вы хотите переключиться:")


@router.message(F.text, NameFile.other_file)
async def handle_state_other_file(message: Message, state: FSMContext):
    filename = message.text.strip()

    file_path = get_file_path(message.from_user.id, filename)

    if not file_path.exists():
        await message.answer("Файл не найден ❌")
        return

    await state.update_data(file_n=filename)
    await state.set_state(NameFile.inner_file)

    await message.answer(f"Вы Переключились в файл под названием {filename} ✅\nПишите заметки ✍️")


@router.message(F.text, NameFile.inner_file)
async def handle_state_inner_file(message: Message, state: FSMContext):
    data = await state.get_data()
    filename = data.get('file_n')

    file_path = get_file_path(message.from_user.id, filename)

    with file_path.open("a", encoding="utf-8") as f:
        f.write(message.text + "\n\n")

    await message.answer("Мысль сохранена ✍️\nНажмите комманду /sendfile если хотите чтоб бот отправил вам файл")




@router.message(Command('merge'))
async def cmd_merge(message:Message,state:FSMContext,command:CommandObject):

    if not command.args:
        await message.answer("Вы не написали название файлов к команде.\nПример: file 1/file 2/file3")
        return

    user_input_file_args = command.args.split("/",maxsplit= 2)

    if len(user_input_file_args) <= 2:
        await message.answer("Для слияния заметок команде нужно 3 файла.Пример: filename/filename_2/filename_3")
        return

    name_1  = user_input_file_args[0].replace(".md","").strip()
    name_2 = user_input_file_args[1].replace(".md","").strip()
    name_3 = user_input_file_args[2].replace('.md',"").strip()

    file_path_1 = get_file_path(message.from_user.id,filename= name_1)
    file_path_2 = get_file_path(message.from_user.id,filename=name_2)
    file_path_3 = get_file_path(message.from_user.id,filename=name_3)

    if not file_path_1.exists():
        await  message.answer(f"Файл {name_1} не найден ❌")
        return

    if not file_path_2.exists():
        await  message.answer(f"Файл {name_2} не найден ❌")
        return


    full_text_1 = file_path_1.read_text(encoding='utf-8')
    full_text_2  = file_path_2.read_text(encoding='utf-8')

    merge_file = full_text_1 + "\n\n" + full_text_2

    file_path_3.write_text(merge_file,encoding='utf-8')
    await message.answer(f"Все заметки успешно объединены в новый файл **{name_3}** ✅")






