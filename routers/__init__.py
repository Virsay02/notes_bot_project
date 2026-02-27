from aiogram import Router

from .change_notes import router as change_notes_router
from .view_notes_files import router as view_notes_file_router
from.main_handlers_commands import router as main_handlers_commands_router


router =  Router()
router.include_routers(
    view_notes_file_router,
            change_notes_router,
            main_handlers_commands_router)