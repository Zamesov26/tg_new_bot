import json
import os
import typing
from logging import getLogger
from urllib.parse import urlencode, urljoin

import aiohttp
from aiohttp import TCPConnector
from aiohttp.client import ClientSession
from pydantic import ValidationError

from app.base.base_accessor import BaseAccessor
from app.tg_api.models import InlineKeyboardMarkup, Message, Update
from app.tg_api.poller import Poller

if typing.TYPE_CHECKING:
    from app.web.app import Application


class MediaSourceNotFound(Exception):
    def __init__(
        self,
        message="Не удалось найти подходящий источник для изображения: отсутствуют file_id, URL и локальный путь.",
    ):
        super().__init__(message)


class MediaItemError(Exception):
    def __init__(self, message="Ошибка формирования одного из media объектов"):
        super().__init__(message)


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

    def build_url(self, method: str) -> str:
        return f"{urljoin(self.server, method)}"

    # TODO от этого надо избавляться
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
        path_image: str,
        caption: str | None = None,
        reply_markup: InlineKeyboardMarkup | None = None,
    ):
        params = {"chat_id": chat_id, "caption": caption or ""}

        if reply_markup:
            params["reply_markup"] = reply_markup.model_dump_json()

        data = aiohttp.FormData()
        data.add_field(
            name="photo",
            value=open(path_image, "rb"),
            filename="file.png",
            content_type="image/png",
        )

        async with self.session.get(
            self._build_query(
                host=self.server,
                method="sendPhoto",
                params=params,
            ),
            data=data,
        ) as response:
            data = await response.json()
            return Message.model_validate(data["result"])

    async def send_media_group(
        self,
        chat_id: int,
        media_items: list[dict],
        reply_markup: InlineKeyboardMarkup | None = None,
    ):
        media_payload = []
        files = {}

        for i, item in enumerate(media_items):
            media = {
                "type": item.get("type", "photo"),
                "caption": item.get("caption", ""),
                # "parse_mode": "HTML"
            }

            if item.get("file_id"):
                media["media"] = item["file_id"]
            elif item.get("url"):
                media["media"] = item["url"]
            elif item.get("file_path") and os.path.exists(item["file_path"]):
                attach_name = f"attach://media{i}"
                media["media"] = attach_name
                files[f"media{i}"] = open(item["file_path"], "rb")
            else:
                raise MediaItemError(
                    f"Не указан file_id, url или file_path для media[{i}]"
                )

            media_payload.append(media)

        form = aiohttp.FormData()
        form.add_field("chat_id", str(chat_id))
        form.add_field("media", json.dumps(media_payload))

        for key, file_obj in files.items():
            form.add_field(
                key, file_obj, filename=f"{key}.jpg", content_type="image/jpeg"
            )

        async with self.session.post(
            self.build_url("sendMediaGroup"), data=form
        ) as resp:
            result = await resp.json()
            for f in files.values():
                f.close()
            return result

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

    async def edit_message_media(
        self,
        message_id: int,
        chat_id: int,
        # должно быть указано либо следующее поле либо прошлые 2
        # inline_message_id: Optional[int] = None,
        *,
        file_id: str | None = None,
        url: str | None = None,
        file_path: str | None = None,
        caption: str | None = None,
        media_type: str = "photo",
        reply_markup: InlineKeyboardMarkup | None = None,
    ):
        media_object = {
            "type": media_type,
            "caption": caption or "",
            "parse_mode": "HTML",
        }
        if file_id:
            media_object["media"] = file_id
            payload = {
                "chat_id": chat_id,
                "message_id": message_id,
                "media": json.dumps(media_object),
                "reply_markup": reply_markup.model_dump_json(),
            }
            async with self.session.post(
                self.build_url(method="editMessageMedia"),
                data=payload,
            ) as resp:
                res = await resp.json()
                return res
        elif url:
            media_object["media"] = url
            payload = {
                "chat_id": chat_id,
                "message_id": message_id,
                "media": json.dumps(media_object),
                "reply_markup": reply_markup.model_dump_json(),
            }
            async with self.session.post(
                self.build_url(method="editMessageMedia"), data=payload
            ) as resp:
                return await resp.json()
        elif file_path and os.path.exists(file_path):
            media_object["media"] = "attach://file"
            form = aiohttp.FormData()
            form.add_field("chat_id", str(chat_id))
            form.add_field("message_id", str(message_id))
            form.add_field("media", json.dumps(media_object))
            form.add_field("reply_markup", reply_markup.model_dump_json())
            with open(file_path, "rb") as file:
                form.add_field(
                    name="file",
                    value=file.read(),
                    filename="example.png",
                    content_type="image/png",
                )

            async with self.session.post(
                self.build_url(method="editMessageMedia"), data=form
            ) as resp:
                return await resp.json()

        raise MediaSourceNotFound()

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
            self.logger.info("geted_update")
            for update in data["result"]:
                self.update_id = int(update["update_id"]) + 1
                try:
                    update_object = Update.model_validate(update)
                except ValidationError as e:
                    self.app.logger.error(e.json())
                    continue
                await self.app.store.bot_manager.add_update(update_object)
