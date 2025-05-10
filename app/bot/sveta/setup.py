import typing

from app.bot.handlers import (
    CommandHandler,
    AddedToChatHandler,
    CallbackQueryHander,
)
from app.bot.sveta.handlers.choosing_program import programs, viewing_details, entering_date
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
    # сhoosing_programm
    app.store.bot_manager.handlers.append(CallbackQueryHander(programs, pattern="^choosing_program"))
    app.store.bot_manager.handlers.append(CallbackQueryHander(viewing_details, pattern="^viewing_details"))
    app.store.bot_manager.handlers.append(CallbackQueryHander(entering_date, pattern="^entering_date"))
    # feedback_input
    app.store.bot_manager.handlers.append(CallbackQueryHander(feedback_input, pattern="^feedback_input"))
    #  promo
    app.store.bot_manager.handlers.append(CallbackQueryHander(promo, pattern="^viewing_faq"))
    # viewing_faq
    app.store.bot_manager.handlers.append(CallbackQueryHander(viewing_faq, pattern="^viewing_faq"))
