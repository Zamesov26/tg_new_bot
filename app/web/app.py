from aiohttp.web import Application as AiohttpApplication
from aiohttp.web import Request as AiohttpRequest
from aiohttp.web import View as AiohttpView
from aiohttp_session import setup as session_setup
from aiohttp_session.cookie_storage import EncryptedCookieStorage

from app.config import Config, setup_config
from app.database.database import Database
from app.store import Store, setup_store
from app.web.logger import setup_logging
from app.web.mw import setup_middlewares
from app.wonderland.setup import setup_sveta

__all__ = ("Application",)


class Application(AiohttpApplication):
    config: Config
    store: Store
    database: Database


class Request(AiohttpRequest):
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
    setup_middlewares(app)
    setup_store(app)
    setup_sveta(app)
    return app
