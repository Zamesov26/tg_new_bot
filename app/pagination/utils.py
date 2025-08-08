from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.database.sqlalchemy_base import BaseModel
    from sqlalchemy.ext.asyncio import AsyncSession


PROGRAM_IMAGE_PATH = "images/programs.png"

def chunk_list(lst, chunk_size):
    return [lst[i : i + chunk_size] for i in range(0, len(lst), chunk_size)]


def generate_base_template(model: type["BaseModel"]):
    return '\n'.join([f"{key}: {{{key}}}" for key in model.__annotations__.keys()]).strip()

def generate_buttons(items, template, chunk_size=2):
    texts = []
    buttons = []
    for item in items:
        texts.append(
            template.format(**vars(item))
        )
        buttons.append([item.title, "details:{id}".format(id=item.id)])
    buttons = chunk_list(buttons, chunk_size)
    return texts, buttons

def generate_pagination_buttons(items, action, id_value, command, model_name, limit):
    paginate_buttons = []
    if action == "after":
        if id_value != 0:
            paginate_buttons.append(
                ["Назад", f"{command}:before:{model_name}:{items[0].id}"]
            )
        if len(items) > limit:
            items.pop()
            paginate_buttons.append(
                ["Далее", f"{command}:after:{model_name}:{items[-1].id}"]
            )
    else:  # before
        if len(items) > limit:
            items.pop()
            paginate_buttons.append(
                ["Назад", f"{command}:before:{model_name}:{items[-1].id}"]
            )
        paginate_buttons.append(
            ["Далее", f"{command}:after:{model_name}:{items[0].id}"]
        )
        items.reverse()
    return paginate_buttons
        
        
        