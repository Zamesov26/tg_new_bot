import typing

from app.bot.handlers import (
    CommandHandler,
    AddedToChatHandler,
    CallbackQueryHander,
)
from app.bot.sveta.handlers.general import bot_help, say_hello, start, info

if typing.TYPE_CHECKING:
    from app.web.app import Application


def setup_sveta(app: "Application"):
    app.store.bot_manager.handlers.append(AddedToChatHandler(say_hello))
    app.store.bot_manager.handlers.append(CommandHandler(bot_help, "help"))
    app.store.bot_manager.handlers.append(CommandHandler(start, "start"))
    app.store.bot_manager.handlers.append(
        CallbackQueryHander(info, pattern="^info")
    )
