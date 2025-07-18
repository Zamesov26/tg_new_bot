import typing

from app.bot_engine.handlers import (
    AddedToChatHandler,
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    TextHandler,
)
from app.questionnaire.mw import add_questionare
from app.wonderland.handlers.choosing_program import (
    entering_date,
    program_details,
    programs,
)
from app.wonderland.handlers.delete_message import delete_message
from app.wonderland.handlers.feedback_input import feedback_input
from app.wonderland.handlers.main_menu import (
    main_menu_callback,
    main_menu_command,
)
from app.wonderland.handlers.order import (
    order_next,
    order_question,
    order_reload,
    order_start,
)
from app.wonderland.handlers.promo import promo
from app.wonderland.handlers.viewing_faq import viewing_faq

if typing.TYPE_CHECKING:
    from app.web.app import Application


def setup_sveta(app: "Application"):
    app.store.bot_manager.handlers.append(AddedToChatHandler(main_menu_command))

    app.store.bot_manager.handlers.append(
        CommandHandler(main_menu_command, command="start")
    )
    app.store.bot_manager.handlers.append(
        CallbackQueryHandler(main_menu_callback, pattern="^main_menu")
    )
    app.store.bot_manager.handlers.append(
        CallbackQueryHandler(programs, pattern="^choosing_program")
    )
    app.store.bot_manager.handlers.append(
        CallbackQueryHandler(program_details, pattern="^program_details:")
    )
    app.store.bot_manager.handlers.append(
        CallbackQueryHandler(entering_date, pattern="^entering_date")
    )
    app.store.bot_manager.handlers.append(
        CallbackQueryHandler(feedback_input, pattern="^feedback_input")
    )
    app.store.bot_manager.handlers.append(
        CallbackQueryHandler(promo, pattern="^promo")
    )
    app.store.bot_manager.handlers.append(
        CallbackQueryHandler(viewing_faq, pattern="^viewing_faq")
    )
    # delete_message
    app.store.bot_manager.handlers.append(
        CallbackQueryHandler(delete_message, pattern="^remove_message")
    )

    order = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(
                add_questionare(order_start, "Бронирование"),
                pattern="^order_start",
            )
        ],
        states={
            "question": [
                TextHandler(order_question),
            ],
            "question_confirmation": [
                CallbackQueryHandler(order_reload, pattern="^question_reload:"),
                CallbackQueryHandler(order_next, pattern="^question_next:"),
            ],
        },
    )
    app.store.bot_manager.handlers.append(order)
    app.store.bot_manager.handlers.append(
        CallbackQueryHandler(order_reload, pattern="^question_reload:")
    )
    app.store.bot_manager.handlers.append(
        CallbackQueryHandler(order_next, pattern="^question_next:")
    )
