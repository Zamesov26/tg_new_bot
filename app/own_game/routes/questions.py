import typing


if typing.TYPE_CHECKING:
    from app.web.app import Application


def setup_routes(app: "Application"):
    from app.own_game.views.questions import CategoryAddView, CategoryListView
    from app.own_game.views.questions import QuestionAddView, QuestionListView

    app.router.add_view("/category.add", CategoryAddView)
    app.router.add_view("/category.list", CategoryListView)

    app.router.add_view("/question.add", QuestionAddView)
    app.router.add_view("/question.list", QuestionListView)
