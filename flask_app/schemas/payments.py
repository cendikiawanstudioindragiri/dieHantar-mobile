from __future__ import annotations

from marshmallow import Schema, fields, validate, validates_schema, ValidationError


class PaymentInitSchema(Schema):
    order_id = fields.String(required=True, validate=validate.Length(min=1, max=64))
    amount = fields.Float(required=True)
    currency = fields.String(required=True, validate=validate.Length(equal=3))
    method = fields.String(load_default="card")

    @validates_schema
    def validate_amount_currency(self, data, **kwargs):
        if data.get("amount") is None or data.get("amount") <= 0:
            raise ValidationError({"amount": ["must_be_positive"]})
        curr = (data.get("currency") or "").upper()
        if not curr.isalpha() or len(curr) != 3:
            raise ValidationError({"currency": ["must_be_iso4217_code"]})
        data["currency"] = curr
