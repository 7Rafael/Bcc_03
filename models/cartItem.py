from db import db

class CartItemModel(db.Model):
    __tablename__ = "cartItem"

    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    cart_id = db.Column(db.Integer, db.ForeignKey("carts.id"), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"), nullable=False)

    cart = db.relationship('CartModel', back_populates='cart_items')
    item = db.relationship('ItemModel', back_populates='cart_items')

    @property
    def total(self):
        return self.quantity * (self.item.price if self.item else 0)
