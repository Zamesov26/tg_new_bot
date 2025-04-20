from marshmallow import Schema, fields


class GameChatIdSchema(Schema):
    chat_id = fields.Int(required=True)


class GameStateSchema(Schema):
    state = fields.Int(Required=True)


class GameSchema(Schema):
    id = fields.Int(required=False)
    chat_id = fields.Int(required=True)
    is_active = fields.Bool(Required=True)
    state = fields.Int(Required=True)
    active_user_id = fields.Int(Required=False)
    responding_user_id = fields.Int(Required=False)
    active_question_id = fields.Int(Required=False)


class GameListSchema(Schema):
    games = fields.Nested(GameSchema, many=True)
