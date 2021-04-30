from app.extensions import ma
from models.user import UserModel
from marshmallow import Schema, fields

class UserSchema(Schema):
    username = fields.String()
    email = fields.Email()
    member_since = fields.DateTime()
    last_seen = fields.DateTime()
    # Use the 'exclude' argument to avoid infinite recursion
    followed = ma.Nested('UserSchema', many=True)
    #followed = fields.Nested(lambda: UserSchema(exclude=("followed",)))
    #friends = fields.List(fields.Nested(lambda: UserSchema()))

"""
    class Meta:
        model = UserModel
        load_only = ("password",)
        dump_only = ("id","confirmed")
        load_instance = True
"""
