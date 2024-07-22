from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import CartModel
from flask_jwt_extended import jwt_required
from flask.views import MethodView
from flask_smorest import Blueprint,abort

from schemas import CartSchema

blp = Blueprint("Cart", __name__, description="Operation on carts")

@blp.route("/cart/<int:cart_id>")
class Cart(MethodView):
    @jwt_required()
    @blp.response(200, CartSchema)
    def get(self, cart_id):
        cart = CartModel.query.get_or_404(cart_id)
        return cart
    @jwt_required()
    def delete(self, cart_id):
         cart = CartModel.query.get_or_404(cart_id)
         db.session.delete(cart)
         db.session.commit()
         return{"message": "Cart deleted."}, 200
    @jwt_required()
    @blp.arguments(CartSchema)
    @blp.response(200, CartSchema)
    def put (self, cart_id, cart_data):
        cart = CartModel.query.get(cart_id)
        if cart:
            cart.updated_date = cart_data["updated_date"]
        else:
            cart = CartModel(id = cart_id, **cart_data)
        db.session.add(cart)
        db.session.commit()
        return cart

@blp.route("/cart")
class CartList(MethodView):
    @blp.response(200, CartSchema(many=True))
    @jwt_required()
    def get(self):
        return CartModel.query.all()
    @jwt_required()
    @blp.arguments(CartSchema)
    @blp.response(201, CartSchema)
    def post(self, cart_data):
        cart = CartModel(**cart_data)
        try:
            db.session.add(cart)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error ocurred while inserting the cart.")

        return cart