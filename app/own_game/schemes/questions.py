from marshmallow import Schema, fields


class CategoryIdSchema(Schema):
    category_id = fields.Int()


class CategorySchema(Schema):
    id = fields.Int(required=False)
    name = fields.Str(required=True)


class CategoryListSchema(Schema):
    themes = fields.Nested(CategorySchema, many=True)


class QuestionSchema(Schema):
    id = fields.Int(required=False)
    title = fields.Str(required=True)
    category_id = fields.Int(required=True)
    answer = fields.Str(required=True)


class QuestionListSchema(Schema):
    questions = fields.Nested(QuestionSchema, many=True)
