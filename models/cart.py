from db import db

class CartModel(db.Model):
    __tablename__ = "carts"

    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    updated_date = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    cart_items = db.relationship('CartItemModel', back_populates='cart')
