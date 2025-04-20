import typing

if typing.TYPE_CHECKING:
    from app.bot.models import (
        UpdateCallBackQuery,
        UpdateMessage,
        UpdateMyChatMember,
    )
    from app.store.store import Store
    
async def say_hello(update: "UpdateMyChatMember", store: "Store", *args):
    text = (
        "Cпасибо, что добавили\n"
        "Бот реагирует на следующие команды\n"
        "/help - для получения списка команд"
    )
    await store.tg_api.send_message(
        chat_id=update.my_chat_member.chat.id,
        text=text,
    )

async def bot_help(update: "UpdateMessage", store: "Store", *args):
    text = "тут должен быть список команд, но его нет("
    await store.tg_api.send_message(
        chat_id=update.message.chat.id,
        text=text,
    )

