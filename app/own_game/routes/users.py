import typing


if typing.TYPE_CHECKING:
    from app.web.app import Application


def setup_routes(app: "Application"):
    from app.own_game.views.users import UserListView

    app.router.add_view("/user.list", UserListView)
