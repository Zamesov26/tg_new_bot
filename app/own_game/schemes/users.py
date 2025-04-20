from marshmallow import Schema, fields


class UserIdSchema(Schema):
    id = fields.Int(Required=True)


class UserSchema(Schema):
    id = fields.Int(required=False)
    name = fields.Str(Required=True)
    tg_id = fields.Int(Required=True)


class UserListSchema(Schema):
    users = fields.Nested(UserSchema, many=True)
