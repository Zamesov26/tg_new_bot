from app.bot.models import UpdateCallBackQuery, UpdateMessage
from app.bot.utils import inline_keyboard_builder
from app.store import Store


async def main_menu(
    update: UpdateCallBackQuery | UpdateMessage, store: "Store", *args
):
    text = (
        "Добро пожаловать в Wonderland — волшебный мир шоу пузырей и весёлых аниматоров!\n"
        "Чем могу помочь?"
    )
    keyboard = inline_keyboard_builder(
        [
            [("🎭 Программы и заказ", "choosing_program")],
            [("🎁 Акции", "promo")],
            [("❓ Частые вопросы", "viewing_faq")],
            [("📞 Связаться с нами", "feedback_input")],
        ]
    )
    if isinstance(update, UpdateCallBackQuery):
        photo_result = await store.tg_api.edit_message_media(
            chat_id=update.get_chat_id(),
            message_id=update.get_message_id(),
            # file_id="AgACAgIAAxkDAAIev2gkRUYxl76b6bLhz1jAuqdSLzs-AAJt7DEbtLQoSUHuX48UhUsSAQADAgADeAADNgQ",
            file_path="images/logo.png",
            caption=text,
            reply_markup=keyboard,
        )
        photo_result
    else:
        photo_result = await store.tg_api.send_photo(
            chat_id=update.get_chat_id(),
            caption=text,
            path_image="images/logo.png",
            reply_markup=keyboard,
        )
        photo_result
