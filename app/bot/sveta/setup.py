import typing

from app.bot.handlers import (
    CommandHandler, AddedToChatHandler,
)
from app.bot.sveta.handlers.general import bot_help, say_hello

if typing.TYPE_CHECKING:
    from app.web.app import Application


def setup_sveta(app: "Application"):
    app.store.bot_manager.handlers.append(AddedToChatHandler(say_hello))
    app.store.bot_manager.handlers.append(CommandHandler(bot_help, "help"))
    # app.store.bot_manager.handlers.append(AddedToChatHandler(say_hello))
    # app.store.bot_manager.handlers.append(CommandHandler(stop, "stop"))
    # conversation = ConversationHander(
    #     entry_points=[CommandHandler(new_game, "start")],
    #     states={
    #         States.PREPARING: [
    #             CallbackQueryHander(added_user, pattern="^add:"),
    #             CallbackQueryHander(go, pattern="^go:"),
    #         ],
    #         States.CHOICE_THEME: [
    #             CallbackQueryHander(choice_theme, pattern="^theme:")
    #         ],
    #         States.CHOICE_QUESTION: [
    #             CallbackQueryHander(choice_price, pattern="^price:"),
    #             CallbackQueryHander(back_to_theme, pattern="^back"),
    #         ],
    #         States.WAITING_PLAYER: [
    #             CallbackQueryHander(click_button, pattern="^click:")
    #         ],
    #         States.WAITING_ANSWER: [TextHandler(some_answer)],
    #     },
    #     fallbacks=[],
    # )
    # app.store.bot_manager.handlers.append(conversation)