import typing

from app.database.database import Database

if typing.TYPE_CHECKING:
    from app.web.app import Application


class Store:
    def __init__(self, app: "Application"):
        from app.admin.accessor import AdminAccessor
        from app.bot_engine.manager import BotManager
        from app.fsm.acceessor import FSMAccessor
        from app.medias.accessor import MediaAccessor
        from app.programs.accessor import ProgramAccessor
        from app.questionnaire.accessor import QuestionnaireAccessor
        from app.tg_api.accessor import TgApiAccessor
        from app.users.accessor import UserAccessor
        from app.templates.accessor import TemplateAccessor

        self.tg_api = TgApiAccessor(app)
        self.bot_manager = BotManager(app)
        self.user = UserAccessor(app)
        self.admin = AdminAccessor(app)
        self.program = ProgramAccessor(app)
        self.fsm = FSMAccessor(app)
        self.questionnaire = QuestionnaireAccessor(app)
        self.media = MediaAccessor(app)
        self.template = TemplateAccessor(app)


def setup_store(app: "Application"):
    app.database = Database(app)
    app.on_startup.append(app.database.connect)
    app.on_cleanup.append(app.database.disconnect)
    app.store = Store(app)
    app.on_startup.append(app.store.bot_manager.start)
    app.on_cleanup.append(app.store.bot_manager.stop)
