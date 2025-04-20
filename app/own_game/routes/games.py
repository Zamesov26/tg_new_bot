import typing

from app.own_game.views.games import (
    GameEndedView,
    GameStateView,
    GameStoppedView,
    GameUserView,
)


if typing.TYPE_CHECKING:
    from app.web.app import Application


def setup_routes(app: "Application"):
    from app.own_game.views.games import GameActiveView

    app.router.add_view("/game.active", GameActiveView)
    app.router.add_view("/game.ended", GameEndedView)
    app.router.add_view("/game.stopped", GameStoppedView)
    app.router.add_view("/game.state", GameStateView)

    app.router.add_view("/game.user", GameUserView)
    # получить игры пользователя
