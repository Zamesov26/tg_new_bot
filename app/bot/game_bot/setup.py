import typing

from app.bot.game_bot.constants import States
from app.bot.game_bot.handlers.general import (
    game_help,
    no_active_game,
    say_hello,
    send_message,
    stop,
)
from app.bot.game_bot.handlers.s0_init import new_game
from app.bot.game_bot.handlers.s1_preparing import added_user, go
from app.bot.game_bot.handlers.s2_3_choice_question import (
    back_to_theme,
    choice_price,
    choice_theme,
)
from app.bot.game_bot.handlers.s4_waiting_player import click_button
from app.bot.game_bot.handlers.s5_waiting_answer import some_answer
from app.bot.handlers import (
    AddedToChatHandler,
    CallbackQueryHander,
    CommandHandler,
    ConversationHander,
    TextHandler,
)

if typing.TYPE_CHECKING:
    from app.web.app import Application


def setup_game_bot(app: "Application"):
    app.store.bot_manager.handlers.append(CommandHandler(game_help, "help"))
    app.store.bot_manager.handlers.append(AddedToChatHandler(say_hello))
    app.store.bot_manager.handlers.append(CommandHandler(stop, "stop"))
    conversation = ConversationHander(
        entry_points=[CommandHandler(new_game, "start")],
        states={
            States.PREPARING: [
                CallbackQueryHander(added_user, pattern="^add:"),
                CallbackQueryHander(go, pattern="^go:"),
            ],
            States.CHOICE_THEME: [
                CallbackQueryHander(choice_theme, pattern="^theme:")
            ],
            States.CHOICE_QUESTION: [
                CallbackQueryHander(choice_price, pattern="^price:"),
                CallbackQueryHander(back_to_theme, pattern="^back"),
            ],
            States.WAITING_PLAYER: [
                CallbackQueryHander(click_button, pattern="^click:")
            ],
            States.WAITING_ANSWER: [TextHandler(some_answer)],
        },
        fallbacks=[],
    )
    app.store.bot_manager.handlers.append(conversation)
