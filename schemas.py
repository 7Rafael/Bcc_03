from marshmallow import Schema, fields

class PlainItemSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)

class PlainStoreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()

class PlainTagSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()

class ItemSchema(PlainItemSchema):
    store_id = fields.Int(required=True, load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)


class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()
    store_id = fields.Int()
    
class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)

class TagSchema(PlainTagSchema):
    store_id = fields.Int(load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)

class TagAndItemSchema(Schema):
    message = fields.Str()
    item = fields.Nested(ItemSchema)
    tag = fields.Nested(TagSchema)

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password =fields.Str(required=True, load_only=True)
    email= fields.Str(required=True)
    role = fields.Str(required=True)
    endereco = fields.Str(required=True)

class UserSchemaLogin(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=False)
    password =fields.Str(required=True, load_only=True)
    email= fields.Str(required=True)
    role = fields.Str(required=False)
    endereco = fields.Str(required=False)

class CartSchema(Schema):
    id = fields.Int(dump_only=True)
    created_date = fields.DateTime(required=True)
    updated_date = fields.DateTime(required=False)
    user_id = fields.Int(required=True)
class CartItemSchema(Schema):
    id = fields.Int(dump_only=True)
    cart_id=fields.Int(required = True)
    item_id=fields.Int(required = True)
    quantity=fields.Int(required = True)
class CartItemSchemaUpdate(Schema):
    cart_id=fields.Int(required = False)
    item_id=fields.Int(required = True)
    quantity=fields.Int(required = True)
