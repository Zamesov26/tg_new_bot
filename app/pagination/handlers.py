from typing import TYPE_CHECKING

from sqlalchemy import select

from app.bot_engine.utils import inline_keyboard_builder
from app.database.utils import resolve_model_by_name
from app.pagination.utils import generate_buttons, generate_base_template, generate_pagination_buttons

if TYPE_CHECKING:
    from app.bot_engine.update_context import Context


# patterns
# paginate:before:Programs:program_id
# paginate:after:Programs:program_id
async def paginate(context: "Context", *args, **kwargs):
    command, action, model_name, ref_id = context.update.callback_query.data.split(":")
    model = resolve_model_by_name(model_name)
    page_size: int = 3
    col_count: int = 2
    limit = page_size * col_count
    
    id_value = int(ref_id)
    
    # TODO: фильтры нужно передавать как параметры. т.к. может понадобиться чтобы отображались только активные элементы
    if action == "after":
        stmt = (select(model).where(model.id > id_value).order_by(model.id.asc()).limit(limit + 1))
    elif action == "before":
        stmt = (select(model).where(model.id < id_value).order_by(model.id.desc()).limit(limit + 1))
    else:
        raise ValueError(f"Unknown pagination action: {action}")
    
    items = list(await context.db_session.scalars(stmt))
    if not items:
        return None
    
    template_model = await context.store.template.get_template(context.db_session, command, model_name)
    paginate_buttons = generate_pagination_buttons(items, action, id_value, command, model_name, limit)
    
    list_template, image_path = None, "images/programs.png"
    list_template = template_model.list_template
    image_file = await context.store.media.get_by_file_path(
        context.db_session, image_path
    )
    
    # if not list_template:
    #     list_template = generate_base_template(model)
        
    texts, buttons = generate_buttons(items, template_model.item_template, chunk_size=col_count)
    if paginate_buttons:
        buttons.append(paginate_buttons)
    
    # TODO: попробовать вынести на отдельный слой
    if context.additional_keyboard:
        buttons.extend(context.additional_keyboard)
    
    keyboard = inline_keyboard_builder(buttons)
    answer = await context.store.tg_api.edit_message_media(
        chat_id=context.event.get_chat_id(),
        message_id=context.event.get_message_id(),
        file_id=image_file.file_id if image_file else None,
        file_path="images/programs.png",
        caption="\n\n".join(texts),
        reply_markup=keyboard,
    )
    return answer
