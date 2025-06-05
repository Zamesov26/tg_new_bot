from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.models import UpdateCallBackQuery, UpdateMessage
from app.bot.utils import inline_keyboard_builder
from app.medias.models import Media
from app.store import Store


async def main_menu(
    update: UpdateCallBackQuery | UpdateMessage,
    store: "Store",
    db_session: AsyncSession,
    *args
):
    message_image_path = "images/logo.png"
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
    image_file = (
        await db_session.execute(
            select(Media).where(Media.file_path == message_image_path)
        )
    ).scalar_one_or_none()

    if isinstance(update, UpdateCallBackQuery):
        answer = await store.tg_api.edit_message_media(
            chat_id=update.get_chat_id(),
            message_id=update.get_message_id(),
            file_id=image_file.file_id if image_file else None,
            file_path=message_image_path,
            caption=text,
            reply_markup=keyboard,
        )
    else:
        answer = await store.tg_api.send_photo(
            chat_id=update.get_chat_id(),
            caption=text,
            path_image=message_image_path,
            file_id=image_file.file_id if image_file else None,
            reply_markup=keyboard,
        )
    if not image_file:
        promo_image = Media(
            title="promo_image",
            file_id=answer["result"]["photo"][0]["file_id"],
            file_path=message_image_path,
        )
        db_session.add(promo_image)
        await db_session.commit()
    return answer
