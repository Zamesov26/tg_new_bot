import typing

from app.bot_engine.utils import inline_keyboard_builder

if typing.TYPE_CHECKING:
    from app.bot_engine.update_context import Context


async def order_start(ctx: "Context", *args, questionnaire: str, **kwargs):
    questionnaire = await ctx.store.questionnaire.get_questionnaire(
        ctx.db_session, questionnaire
    )
    if not questionnaire:
        return await ctx.store.tg_api.send_message(
            chat_id=ctx.update.callback_query.message.chat.id,
            text="Внутренняя ошибка, попробуйте позже",
        )

    question_ids = list(
        await ctx.store.questionnaire.get_question_ids(
            db_session=ctx.db_session, questionnaire_id=questionnaire.id
        )
    )[::-1]
    form_instance = await ctx.store.questionnaire.create_form_instance(
        db_session=ctx.db_session,
        user_id=ctx.user_id,
        questionare_id=questionnaire.id,
    )

    firs_question = question_ids.pop()
    new_data = (ctx.fsm_data or {}) | {
        "instance": str(form_instance.id),
        "questions": question_ids,
        "current_question": firs_question,
    }
    await ctx.store.fsm.update_fsm(
        ctx=ctx,
        new_state="question",
        new_data=new_data,
    )
    question = await ctx.store.questionnaire.get_question(
        db_session=ctx.db_session, question_id=firs_question
    )
    await ctx.store.tg_api.send_message(ctx.chat_id, question.text)


async def order_question(ctx: "Context", *args, **kwargs):
    instance_id = ctx.fsm_data.get("instance")
    texts = [
        "Ваш ответ:",
        ctx.update.message.text,
    ]
    buttons = [
        [
            ["Изменить", f"question_reload:{instance_id}"],
            ["Далее", f"question_next:{instance_id}"],
        ],
    ]
    question_id = ctx.fsm_data.get("current_question")
    await ctx.store.questionnaire.create_answer(
        ctx,
        question_id=question_id,
        form_instance_id=instance_id,
        value=ctx.update.message.text,
    )

    keyboard = inline_keyboard_builder(buttons)
    await ctx.store.tg_api.delete_message(
        chat_id=ctx.update.message.chat.id,
        message_id=ctx.update.message.message_id,
    )
    await ctx.store.tg_api.send_message(
        ctx.chat_id, "\n".join(texts), reply_markup=keyboard
    )
    await ctx.store.fsm.update_fsm(
        ctx=ctx, new_state="question_confirmation", new_data=ctx.fsm_data
    )


async def order_next(ctx: "Context", *args, **kwargs):
    _, callback_instance = ctx.update.callback_query.data.split(":")
    instance = ctx.fsm_data.get("instance")
    if not instance or instance != callback_instance:
        return await ctx.store.tg_api.delete_message(
            ctx.chat_id,
            ctx.update.callback_query.message.message_id,
        )
    await ctx.store.tg_api.edit_message_reply_markup(
        message_id=ctx.update.callback_query.message.message_id,
        chat_id=ctx.update.callback_query.message.chat.id,
        reply_markup=None,
    )

    question_ids = ctx.fsm_data.get("questions")
    if not question_ids:
        if not ctx.fsm_data:
            ctx.fsm_data = {}
        ctx.fsm_data.pop("instance")
        ctx.fsm_data.pop("questions")
        ctx.fsm_data.pop("current_question")
        await ctx.store.fsm.update_fsm(
            ctx=ctx,
            new_state=None,
            new_data=ctx.fsm_data,
        )
        keyboard = inline_keyboard_builder([[["🔙 Меню", f"main_menu"]]])
        # Оповещение админов
        return await ctx.store.tg_api.send_message(
            ctx.chat_id, text="Анкета отправлена", reply_markup=keyboard
        )

    question_id = question_ids.pop()
    question = await ctx.store.questionnaire.get_question(
        db_session=ctx.db_session, question_id=question_id
    )
    await ctx.store.fsm.update_fsm(
        ctx=ctx,
        new_state="question",
        new_data=ctx.fsm_data
        | {
            "current_question": question.id,
        },
    )
    return await ctx.store.tg_api.send_message(ctx.chat_id, question.text)


async def order_reload(ctx: "Context", *args, **kwargs):
    _, callback_instance = ctx.update.callback_query.data.split(":")
    instance = ctx.fsm_data.get("instance")
    if not instance or instance != callback_instance:
        return await ctx.store.tg_api.delete_message(
            ctx.chat_id,
            ctx.update.callback_query.message.message_id,
        )
    await ctx.store.fsm.update_fsm(
        ctx=ctx,
        new_state="question",
        new_data=ctx.fsm_data,
    )
    return await ctx.store.tg_api.delete_message(
        chat_id=ctx.update.callback_query.message.chat.id,
        message_id=ctx.update.callback_query.message.message_id,
    )
