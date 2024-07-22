from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import CartItemModel
from flask_jwt_extended import jwt_required
from flask.views import MethodView
from flask_smorest import Blueprint,abort

from schemas import CartItemSchema, CartItemSchemaUpdate

blp = Blueprint("CartItem", __name__, description="Operation on cartItems")

@blp.route("/cartItem/<int:cartItem_id>")
class CartItem(MethodView):
    @jwt_required()
    @blp.response(200, CartItemSchema)
    def get(self, cartItem_id):
        cartItem = CartItemModel.query.get_or_404(cartItem_id)
        return cartItem
    @jwt_required()
    def delete(self, cartItem_id):
         cartItem = CartItemModel.query.get_or_404(cartItem_id)
         db.session.delete(cartItem)
         db.session.commit()
         return{"message": "CartItem deleted."}, 200
    @jwt_required()
    @blp.arguments(CartItemSchemaUpdate)
    @blp.response(200, CartItemSchemaUpdate)
    def put (self, cartItem_id, cartItem_data):
        cartItem = CartItemModel.query.get(cartItem_id)
        if cartItem:
            cartItem.quantity = cartItem_data["quantity"]
        else:
            cartItem = CartItemModel(id = cartItem_id, **cartItem_data)
        db.session.add(cartItem)
        db.session.commit()
        return cartItem

@blp.route("/cartItem")
class CartItemList(MethodView):
    @blp.response(200, CartItemSchema(many=True))
    @jwt_required()
    def get(self):
        return CartItemModel.query.all()
    @jwt_required()
    @blp.arguments(CartItemSchema)
    @blp.response(201, CartItemSchema)
    def post(self, cartItem_data):
        cart_item = CartItemModel(**cartItem_data)
        db.session.add(cart_item)
        db.session.commit()
        return cart_item