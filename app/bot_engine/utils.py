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
    lst: list[list[tuple[str | int, str]]],
) -> InlineKeyboardMarkup:
    res_keyboard = []
    for row in lst:
        row_keyboard = []
        for text, callback_data in row:
            row_keyboard.append(
                InlineKeyboardButton(
                    text=str(text), callback_data=callback_data
                )
            )
        res_keyboard.append(row_keyboard)
    return InlineKeyboardMarkup(inline_keyboard=res_keyboard)


def inline_keyboard_game_builder(
    lst: TextKeyBoard, prefix="", sep=":", postfix=""
):
    res_keyboard = []
    for row in lst:
        row_keyboard = []
        for col in row:
            if isinstance(col, int | str):
                text = str(col)
                callback_data = prefix + sep + str(col)
                if postfix:
                    callback_data += sep + postfix
            else:
                text, callback_data = col
            row_keyboard.append((str(text), callback_data))
        res_keyboard.append(row_keyboard)
    return inline_keyboard_builder(res_keyboard)
