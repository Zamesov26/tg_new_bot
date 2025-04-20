import typing


if typing.TYPE_CHECKING:
    from app.web.app import Application

__all__ = ("setup_routes",)


def setup_routes(app: "Application"):
    from app.own_game.routes.questions import (
        setup_routes as setup_question_routes,
    )
    from app.own_game.routes.games import setup_routes as setup_game_routes
    from app.own_game.routes.users import setup_routes as setup_user_routes

    setup_user_routes(app)
    setup_question_routes(app)
    setup_game_routes(app)
