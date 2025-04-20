from aiohttp.web_exceptions import HTTPBadRequest, HTTPConflict, HTTPNotFound
from aiohttp_apispec import (
    docs,
    querystring_schema,
    request_schema,
    response_schema,
)
from app.own_game.schemes.questions import (
    CategoryIdSchema,
    CategoryListSchema,
    CategorySchema,
    QuestionListSchema,
    QuestionSchema,
)
from app.web.app import View
from app.web.mixins import AuthRequiredMixin
from app.web.utils import json_response


class CategoryAddView(AuthRequiredMixin, View):
    @docs(tags=["Category"])
    @request_schema(CategorySchema)
    @response_schema(CategorySchema)
    async def post(self):
        category = await self.store.question.get_category_by_name(
            self.data["name"]
        )
        if category:
            raise HTTPConflict
        category = await self.store.question.create_category(self.data["name"])

        return json_response(CategorySchema().dump(category))


class CategoryListView(AuthRequiredMixin, View):
    @docs(tags=["Category"])
    @response_schema(CategoryListSchema)
    async def get(self):
        categories = await self.store.question.list_categories()
        categories = [
            CategorySchema().dump(category) for category in categories
        ]
        return json_response({"categories": categories})


class QuestionAddView(AuthRequiredMixin, View):
    @docs(tags=["Question"])
    @request_schema(QuestionSchema)
    @response_schema(QuestionSchema)
    async def post(self):
        question = self.data
        db_session = self.database.session()
        async with db_session.begin():
            if not await self.store.question.get_category_by_id(
                db_session, category_id=int(question["category_id"])
            ):
                raise HTTPNotFound

            raw_question = await self.store.question.create_question(
                answer=question["answer"],
                category_id=question["category_id"],
                title=question["title"],
            )

        return json_response(QuestionSchema().dump(raw_question))


class QuestionListView(AuthRequiredMixin, View):
    @docs(tags=["Question"])
    @querystring_schema(CategoryIdSchema)
    @response_schema(QuestionListSchema)
    async def get(self):
        category_id = int(self.request.query.get("category_id"))
        db_session = self.database.session()
        async with db_session.begin():
            questions = await self.store.question.list_questions(
                db_session=db_session, category_id=category_id
            )

        raw_questions = [
            QuestionSchema().dump(question) for question in questions
        ]
        return json_response(data={"questions": raw_questions})
