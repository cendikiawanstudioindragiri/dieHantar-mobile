from __future__ import annotations

from marshmallow import Schema, fields, validate


class UserLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=6, max=128))
