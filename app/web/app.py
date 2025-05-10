from aiohttp.web import (
    Application as AiohttpApplication,
    Request as AiohttpRequest,
    View as AiohttpView,
)
from aiohttp_apispec import setup_aiohttp_apispec
from aiohttp_session import setup as session_setup
from aiohttp_session.cookie_storage import EncryptedCookieStorage

from app.admin.models import AdminModel
from app.bot.sveta.setup import setup_sveta
from app.config import Config, setup_config
from app.database.database import Database
from app.store import Store, setup_store
from app.web.logger import setup_logging
from app.web.mw import setup_middlewares
from app.web.routes import setup_routes

# from .routes import setup_routes

__all__ = ("Application",)


class Application(AiohttpApplication):
    config: Config
    store: Store
    database: Database


class Request(AiohttpRequest):
    admin: AdminModel | None = None

    @property
    def app(self) -> Application:
        return super().app()


class View(AiohttpView):
    @property
    def request(self) -> Request:
        return super().request

    @property
    def database(self) -> Database:
        return self.request.app.database

    @property
    def store(self) -> Store:
        return self.request.app.store

    @property
    def data(self) -> dict:
        return self.request.get("data", {})


app = Application()


def setup_app(config_path: str) -> Application:
    setup_logging(app)
    setup_config(app, config_path)
    session_setup(app, EncryptedCookieStorage(app.config.session.key))
    # setup_aiohttp_apispec(
    #     app,
    #     title="TG own-game Bot",
    #     url="/docs/json",
    #     swagger_path="/docs",
    #     # prefix="/v1",
    # )
    # setup_routes(app)
    setup_middlewares(app)
    setup_store(app)
    setup_sveta(app)
    return app
