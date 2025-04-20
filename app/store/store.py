import typing

from app.admin.accessor import AdminAccessor
from app.database.database import Database
from app.own_game.accessors import GameAccessor, QuestionAccessor, UserAccessor
from app.rabbit.accessor import RabbitAccessor
from app.radis.accessor import RedisAccessor

if typing.TYPE_CHECKING:
    from app.web.app import Application


class Store:
    def __init__(self, app: "Application"):
        from app.bot.bot_manager import BotManager
        from app.tg_api.accessor import TgApiAccessor

        self.admins = AdminAccessor(app)
        self.tg_api = TgApiAccessor(app)
        self.bot_manager = BotManager(app)
        self.question = QuestionAccessor(app)
        self.game = GameAccessor(app)
        self.user = UserAccessor(app)
        self.redis = RedisAccessor(app)
        self.rabbit = RabbitAccessor(app)


def setup_store(app: "Application"):
    app.database = Database(app)
    app.on_startup.append(app.database.connect)
    app.on_cleanup.append(app.database.disconnect)
    app.store = Store(app)
    app.on_startup.append(app.store.bot_manager.start)
    app.on_cleanup.append(app.store.bot_manager.stop)
