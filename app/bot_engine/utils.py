import typing

from app.tg_api.models import InlineKeyboardButton, InlineKeyboardMarkup

TextKeyBoard = typing.Annotated[
    list[list[str | int | tuple[int | str, int | str]]],
    (
        "список названий и разметка для формирования inline клавиатуры "
        "eсли callback не задан то сформирует по шаблону"
    ),
]


def inline_keyboard_builder(
    lst,  # list[list[list[str | int, str, str | None]]],
) -> InlineKeyboardMarkup:
    res_keyboard = []
    for row in lst:
        row_keyboard = []
        for i in row:
            if len(i) == 2:
                i.append("")
        for text, callback_data, url in row:
            row_keyboard.append(
                InlineKeyboardButton(
                    text=str(text), callback_data=callback_data, url=url
                )
            )
        res_keyboard.append(row_keyboard)
    return InlineKeyboardMarkup(inline_keyboard=res_keyboard)