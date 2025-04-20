import typing

from app.bot.utils import inline_keyboard_builder
from app.tg_api.models import InlineKeyboardMarkup

if typing.TYPE_CHECKING:
    from app.own_game.models.questions import Category


def players_to_text_grid(players) -> str:
    sorted_players = sorted(
        players,
        key=lambda x: x[3],
    )
    return "\n".join(
        [
            (f"{user_name:<11} {points}")
            for (_, user_name, _, points) in sorted_players
        ]
    )


def get_category_keyboard(
    themes: list["Category"], player_tg_id: int, cols=3
) -> InlineKeyboardMarkup:
    res = []
    for i in range(0, len(themes), cols):
        row = [
            (theme.name, f"theme:{player_tg_id}:{theme.id}")
            for theme in themes[i : i + cols]
        ]
        res.append(row)
    return inline_keyboard_builder(res)
