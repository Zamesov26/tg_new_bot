import typing

if typing.TYPE_CHECKING:
    from aiohttp.web_app import Application

__all__ = ("setup_routes",)


def setup_routes(app: "Application"):
    from app.admin.routes import setup_routes as admin_setup_routes
    from app.own_game.routes import setup_routes as setup_own_game_routes

    # import app.users.routes

    admin_setup_routes(app)
    setup_own_game_routes(app)

    # app.users.routes.register_urls(application)
