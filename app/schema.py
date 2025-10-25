from marshmallow import Schema, fields, ValidationError, validates, pre_load


class ProductSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    category = fields.Str(allow_none=True, missing=None)
    available = fields.Bool(missing=True)
    price = fields.Float(missing=0.0)
    description = fields.Str(missing="")

    @validates("name")
    def validate_name(self, value: str) -> None:
        if not value or not value.strip():
            raise ValidationError("name must be a non-empty string")

    @pre_load
    def strip_strings(self, data, **kwargs):  # type: ignore[no-untyped-def]
        for k in ["name", "category", "description"]:
            if isinstance(data.get(k), str):
                data[k] = data[k].strip()
        return data


product_schema = ProductSchema()
products_schema = ProductSchema(many=True)
