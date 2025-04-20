from aiohttp_apispec import docs, response_schema
from app.own_game.schemes.users import UserListSchema, UserSchema
from app.web.app import View
from app.web.mixins import AuthRequiredMixin
from app.web.utils import json_response


class UserListView(AuthRequiredMixin, View):
    @docs(tags=["User"])
    @response_schema(UserListSchema)
    async def get(self):
        db_session = self.database.session()
        async with db_session.begin():
            users = await self.store.user.get_all(db_session)

        row_users = [UserSchema().dump(user) for user in users]
        return json_response({"users": row_users})
