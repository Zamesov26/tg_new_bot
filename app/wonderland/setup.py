import typing


from app.bot_engine.handlers import (
    AddedToChatHandler,
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    TextHandler,
)
from app.questionnaire.mw import inject_kwargs
from app.wonderland.handlers.choosing_program import program_details, programs
from app.wonderland.handlers.contacts import contacts
from app.wonderland.handlers.delete_message import delete_message
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
    from sqlalchemy.ext.asyncio import AsyncSession

def setup_wonderland(app: "Application", prefix_pattern: str = ""):
    # pages
    db_session: "AsyncSession" = app.database.session()
    app.store.bot_manager.handlers.append(
        CommandHandler(
            callback=main_menu_command,
            command="start",
        )
    )
    app.store.bot_manager.handlers.append(
        CallbackQueryHandler(
            callback=main_menu_callback,
            pattern="^main_menu",
        )
    )
    app.store.bot_manager.handlers.append(
        CallbackQueryHandler(
            callback=contacts,
            pattern="^contacts",
        )
    )

    # pagination tables
    app.store.bot_manager.handlers.append(
        CallbackQueryHandler(
            callback=programs,
            pattern="^choosing_program",
        )
    )
    app.store.bot_manager.handlers.append(
        CallbackQueryHandler(callback=promo, pattern="^promo")
    )
    app.store.bot_manager.handlers.append(
        CallbackQueryHandler(callback=viewing_faq, pattern="^viewing_faq")
    )

    #  functions
    app.store.bot_manager.handlers.append(
        CallbackQueryHandler(
            callback=program_details, pattern="^program_details:"
        )
    )
    app.store.bot_manager.handlers.append(
        CallbackQueryHandler(callback=delete_message, pattern="^remove_message")
    )
    app.store.bot_manager.handlers.append(
        AddedToChatHandler(callback=main_menu_command)
    )

    # order conversation
    order = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(
                callback=inject_kwargs(
                    order_start, questionare_name="Бронирование"
                ),
                pattern="^order_start:",
            )
        ],
        states={
            "question": [
                TextHandler(callback=order_question),
            ],
            "question_confirmation": [
                CallbackQueryHandler(
                    callback=order_reload, pattern="^question_reload:"
                ),
                CallbackQueryHandler(
                    callback=order_next, pattern="^question_next:"
                ),
            ],
        },
    )
    app.store.bot_manager.handlers.append(order)
