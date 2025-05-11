import typing

from app.bot.handlers import (
    AddedToChatHandler,
    CallbackQueryHander,
    CommandHandler,
)
from app.bot.sveta.handlers.choosing_program import (
    entering_date,
    programs,
    viewing_details,
)
from app.bot.sveta.handlers.delete_message import delete_message
from app.bot.sveta.handlers.feedback_input import feedback_input
from app.bot.sveta.handlers.general import bot_help, say_hello
from app.bot.sveta.handlers.main_menu import main_menu
from app.bot.sveta.handlers.promo import promo
from app.bot.sveta.handlers.viewing_faq import viewing_faq

if typing.TYPE_CHECKING:
    from app.web.app import Application


def setup_sveta(app: "Application"):
    app.store.bot_manager.handlers.append(AddedToChatHandler(say_hello))
    app.store.bot_manager.handlers.append(CommandHandler(bot_help, "help"))
    app.store.bot_manager.handlers.append(CommandHandler(main_menu, "start"))
    app.store.bot_manager.handlers.append(
        CallbackQueryHander(main_menu, pattern="^main_menu")
    )
    # сhoosing_programm
    app.store.bot_manager.handlers.append(
        CallbackQueryHander(programs, pattern="^choosing_program")
    )
    app.store.bot_manager.handlers.append(
        CallbackQueryHander(viewing_details, pattern="^viewing_details:")
    )
    app.store.bot_manager.handlers.append(
        CallbackQueryHander(entering_date, pattern="^entering_date")
    )
    # feedback_input
    app.store.bot_manager.handlers.append(
        CallbackQueryHander(feedback_input, pattern="^feedback_input")
    )
    #  promo
    app.store.bot_manager.handlers.append(
        CallbackQueryHander(promo, pattern="^promo")
    )
    # viewing_faq
    app.store.bot_manager.handlers.append(
        CallbackQueryHander(viewing_faq, pattern="^viewing_faq")
    )
    # delete_message
    app.store.bot_manager.handlers.append(
        CallbackQueryHander(delete_message, pattern="^remove_message")
    )
