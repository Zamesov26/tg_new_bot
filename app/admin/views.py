from aiohttp.web_exceptions import HTTPForbidden
from aiohttp_apispec import docs, request_schema, response_schema
from aiohttp_session import get_session

from app.admin.models import hash_password
from app.admin.schemes import AdminSchema
from app.web.app import View
from app.web.mixins import AuthRequiredMixin
from app.web.utils import json_response


class AdminLoginView(View):
    @docs(tags=["Admin"])
    @request_schema(AdminSchema)
    @response_schema(AdminSchema, 200)
    async def post(self):
        admin = await self.store.admins.get_by_email(self.data["email"])
        if not admin:
            raise HTTPForbidden
        if admin.password != hash_password(self.data["password"]):
            raise HTTPForbidden

        admin_row = AdminSchema().dump(admin)
        response = json_response(data=admin_row)

        session = await get_session(request=self.request)
        session["admin"] = admin_row

        return response


class AdminCurrentView(AuthRequiredMixin, View):
    @docs(tags=["Admin"])
    @response_schema(AdminSchema, 200)
    async def get(self):
        return json_response(data=AdminSchema().dump(self.request.admin))
