import marshmallow as ma


class ErrorSchema(ma.Schema):
    code = ma.fields.String()
    message = ma.fields.String()
    errors = ma.fields.List(ma.fields.Dict())
