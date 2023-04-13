from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)




class Restaurant(db.Model, SerializerMixin):
    __tablename__ = "restaurants"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)

    restaurantpizzas = db.relationship('RestaurantPizza', backref='restaurant')
    pizzas = association_proxy('Pizza', 'restaurants')

    def __repr__(self):
        return f'<Restaurant {self.name}, ID: {self.id}>'
    

class Pizza(db.Model, SerializerMixin):
    __tablename__ = "pizzas"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    restaurantpizzas = db.relationship('RestaurantPizza', backref='pizza')
    restaurants = association_proxy('Restaurant', 'pizzas')

    serialize_rules = ('-created_at', '-updated_at')

    def __repr__(self):
        return f'<Pizza {self.name}, ingredients: {self.ingredients}, ID: {self.id}>'
    
class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = "restaurantpizzas"

    id = db.Column(db.Integer, primary_key=True)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))
    price = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    serialize_rules = ('-created_at', '-updated_at', '-restaurant.restaurantpizzas', '-pizza.restaurantpizzas')

    @validates('price')
    def validate_price(self, key, price):
        if price < 1 or price > 30:
            raise ValueError('Price must be between 1 and 30.')
        else:
            return price

    def __repr__(self):
        return f'<RestaurantPizza ID: {self.id}>'
