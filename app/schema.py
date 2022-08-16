from marshmallow import Schema, fields

#Define User response schema
class UserResponseSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Integer(dump_only=True)
    email = fields.Email(required=True)
    password = fields.String(required=True, load_only=True)

#Define Bucketlist item response schema
class ItemResponseSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    date_created = fields.DateTime()
    date_modified = fields.DateTime()
    created_by = fields.Nested(lambda: "UserResponseSchema", only=("id","email,"))
    done = fields.Boolean(default=False)