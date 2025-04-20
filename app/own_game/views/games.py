from aiohttp_apispec import (
    docs,
    querystring_schema,
    request_schema,
    response_schema,
)
from app.own_game.schemes.games import (
    GameListSchema,
    GameSchema,
    GameStateSchema,
)
from app.own_game.schemes.users import UserIdSchema
from app.web.app import View
from app.web.mixins import AuthRequiredMixin
from app.web.utils import json_response


class GameStateView(AuthRequiredMixin, View):
    @docs(tags=["Game"])
    @querystring_schema(GameStateSchema)
    @response_schema(GameListSchema)
    async def get(self):
        db_session = self.database.session()
        state = self.request.query.get("state")
        if not state:
            return
        async with db_session.begin():
            games = await self.store.game.get_games_by_state(
                db_session, int(state)
            )

        row_games = [GameSchema().dump(game) for game in games]
        return json_response({"games": row_games})


class GameActiveView(AuthRequiredMixin, View):
    @docs(tags=["Game"])
    @response_schema(GameListSchema)
    async def get(self):
        db_session = self.database.session()
        async with db_session.begin():
            games = await self.store.game.get_active_games(db_session)

        row_games = [GameSchema().dump(game) for game in games]
        return json_response({"games": row_games})


class GameEndedView(AuthRequiredMixin, View):
    @docs(tags=["Game"])
    @response_schema(GameListSchema)
    async def get(self):
        db_session = self.database.session()
        async with db_session.begin():
            games = await self.store.game.get_ended_games(db_session)

        row_games = [GameSchema().dump(game) for game in games]
        return json_response({"games": row_games})


class GameStoppedView(AuthRequiredMixin, View):
    @docs(tags=["Game"])
    @response_schema(GameListSchema)
    async def get(self):
        db_session = self.database.session()
        async with db_session.begin():
            games = await self.store.game.get_stopped_games(db_session)

        row_games = [GameSchema().dump(game) for game in games]
        return json_response({"games": row_games})


class GameUserView(AuthRequiredMixin, View):
    @docs(tags=["Game", "User"])
    @querystring_schema(UserIdSchema)
    @response_schema(GameListSchema)
    async def get(self):
        db_session = self.database.session()
        user_id = self.request.query.get("id")
        if not user_id:
            return
        async with db_session.begin():
            games = await self.store.game.get_user_games(
                db_session, int(user_id)
            )

        row_games = [GameSchema().dump(game) for game in games]
        return json_response({"games": row_games})
