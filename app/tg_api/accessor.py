import json
from logging import getLogger
import typing
from urllib.parse import urlencode, urljoin

from aiohttp import TCPConnector
from aiohttp.client import ClientSession
from pydantic import ValidationError

from app.base.base_accessor import BaseAccessor
from app.tg_api.models import (
    InlineKeyboardMarkup,
    Message,
    Update,
)
from app.tg_api.poller import Poller

if typing.TYPE_CHECKING:
    from app.web.app import Application


class TgApiAccessor(BaseAccessor):
    def __init__(self, app: "Application", *args, **kwargs):
        super().__init__(app, *args, **kwargs)

        self.logger = getLogger("TgApiAccessor")
        self.session: ClientSession
        self.poller: Poller
        self.server = f"https://api.telegram.org/bot{app.config.bot.token}/"
        self.update_id = 0
        self.allowed_updates = []

    async def connect(self, app: "Application"):
        self.session = ClientSession(connector=TCPConnector(verify_ssl=False))

        self.poller = Poller(app.store)
        self.logger.info("start tg polling")
        self.poller.start()

    async def disconnect(self, app: "Application"):
        if self.session:
            await self.session.close()

        if self.poller:
            await self.poller.stop()
        self.logger.info("stopped tg polling")

    @staticmethod
    def _build_query(host: str, method: str, params: dict) -> str:
        return f"{urljoin(host, method)}?{urlencode(params)}"

    async def send_message(
        self, chat_id, text, reply_markup: InlineKeyboardMarkup | None = None
    ):
        params = {
            "chat_id": chat_id,
            "text": text,
        }

        if reply_markup:
            params["reply_markup"] = reply_markup.model_dump_json()

        async with self.session.get(
            self._build_query(
                host=self.server,
                method="sendMessage",
                params=params,
            )
        ) as response:
            data = await response.json()
            print(data)
            return Message.model_validate(data["result"])

    async def send_photo(
        self,
        chat_id: int,
        photo_url: str,
        caption: str,
        reply_markup: InlineKeyboardMarkup | None = None,
    ):
        params = {"chat_id": chat_id, "caption": caption, "photo": photo_url}

        if reply_markup:
            params["reply_markup"] = reply_markup.model_dump_json()

        async with self.session.get(
            self._build_query(
                host=self.server,
                method="sendPhoto",
                params=params,
            )
        ) as response:
            data = await response.json()
            return Message.model_validate(data["result"])

    async def edit_message_text(
        self,
        text: str,
        message_id: int,
        chat_id: int,
        # должно быть указано либо следующее поле либо прошлые 2
        # inline_message_id: Optional[int] = None,
        reply_markup: InlineKeyboardMarkup | None = None,
    ):
        params = {"text": text, "message_id": message_id, "chat_id": chat_id}
        if reply_markup:
            params["reply_markup"] = reply_markup.model_dump_json()

        async with self.session.get(
            self._build_query(
                host=self.server,
                method="editMessageText",
                params=params,
            )
        ) as response:
            return await response.json()

    async def edit_message_caption(
        self,
        caption: str,
        message_id: int,
        chat_id: int,
        # должно быть указано либо следующее поле либо прошлые 2
        # inline_message_id: Optional[int] = None,
        reply_markup: InlineKeyboardMarkup | None = None,
    ):
        params = {
            "caption": caption,
            "message_id": message_id,
            "chat_id": chat_id,
        }
        if reply_markup:
            params["reply_markup"] = reply_markup.model_dump_json()

        async with self.session.get(
            self._build_query(
                host=self.server,
                method="editMessageCaption",
                params=params,
            )
        ) as response:
            return await response.json()

    async def delete_message(self, chat_id, message_id):
        params = {"chat_id": chat_id, "message_id": message_id}
        async with self.session.get(
            self._build_query(
                host=self.server,
                method="deleteMessage",
                params=params,
            )
        ) as response:
            return await response.json()

    async def edit_message_reply_markup(
        self,
        chat_id: int,
        message_id: int,
        reply_markup: InlineKeyboardMarkup | None = None,
    ):
        params = {"chat_id": chat_id, "message_id": message_id}
        if reply_markup:
            params["reply_markup"] = reply_markup.model_dump_json()
        else:
            params["reply_markup"] = InlineKeyboardMarkup(
                inline_keyboard=[]
            ).model_dump_json()
        async with self.session.get(
            self._build_query(
                host=self.server,
                method="editMessageReplyMarkup",
                params=params,
            )
        ) as response:
            res = await response.json()
            return res

    async def answer_callback_query(self, callback_query_id: str):
        async with self.session.get(
            self._build_query(
                host=self.server,
                method="answerCallbackQuery",
                params={"callback_query_id": callback_query_id},
            )
        ) as response:
            return await response.json()

    async def poll(self):
        async with self.session.get(
            self._build_query(
                host=self.server,
                method="getUpdates",
                params={
                    "offset": self.update_id,
                    "timeout": 30,
                    # "limit": 100,
                    "allowed_updates": [],
                },
            )
        ) as response:
            data = await response.json()
            self.logger.info("getet_update")
            for update in data["result"]:
                self.update_id = int(update["update_id"]) + 1
                try:
                    update_object = Update.model_validate(update)
                except ValidationError as e:
                    self.app.logger.error(e.json())
                    continue
                await self.app.store.bot_manager.add_update(update_object)
