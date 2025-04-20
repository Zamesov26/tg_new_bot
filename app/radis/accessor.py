from logging import getLogger
import typing

import redis

from app.base.base_accessor import BaseAccessor

if typing.TYPE_CHECKING:
    from app.web.app import Application


class RedisAccessor(BaseAccessor):
    def __init__(self, app: "Application", *args, **kwargs):
        super().__init__(app)
        # todo брать настройки из config'a
        self.r = redis.Redis()
        self.logger = getLogger("RedisAccessor")

    async def connect(self, *args, **kwargs):
        self.logger.info("start RedisAccessor")

    def clear_chat(self, chat_id):
        self.delete_active_players(chat_id)
        self.delete_responding_user(chat_id)
        self.delete_state(chat_id)

    def get_last_message(
        self, chat_id: int, with_deletion: bool = False
    ) -> int | None:
        message_id = self.r.get(f"last_message:{chat_id}")

        if not message_id:
            return None

        if with_deletion:
            self.r.delete(f"last_message:{chat_id}")

        return int(message_id)

    def set_last_message(self, chat_id: int, message_id: int):
        self.r.set(f"last_message:{chat_id}", message_id)

    def get_state(self, chat_id):
        state = self.r.get(f"state:{chat_id}")
        if not state:
            return None
        return int(state)

    def delete_state(self, chat_id):
        self.r.delete(f"state:{chat_id}")

    def set_state(self, chat_id: int, state: int):
        self.r.set(f"state:{chat_id}", state)

    def add_active_players(self, chat_id, active_users_tg_ids):
        if active_users_tg_ids:
            self.r.sadd(f"active_players:{chat_id}", *active_users_tg_ids)

    def get_active_players(self, chat_id):
        return [int(i) for i in self.r.smembers(f"active_players:{chat_id}")]

    def is_active_players(self, chat_id, user_tg_id):
        return self.r.sismember(f"active_players:{chat_id}", user_tg_id)

    def delete_active_players(self, chat_id):
        self.r.delete(f"active_players:{chat_id}")

    def set_responding_user(self, chat_id, user_tg_id):
        self.r.set(f"responding_user:{chat_id}", user_tg_id)

    def get_responding_user(self, chat_id):
        return int(self.r.get(f"responding_user:{chat_id}"))

    def delete_responding_user(self, chat_id):
        self.r.delete(f"responding_user:{chat_id}")
