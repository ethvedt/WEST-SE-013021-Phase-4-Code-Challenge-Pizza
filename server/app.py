#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api

from models import db, Restaurant, RestaurantPizza, Pizza

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Code challenge</h1>'

@app.route('/restaurants')
def restaurants():
    rests = Restaurant.query.all()
    rest_list = [rest.to_dict(only=('id', 'name', 'address')) for rest in rests]
    return rest_list

@app.route('/restaurants/<int:id>', methods=['GET', 'DELETE'])
def restaurant_by_id(id):
    rest = Restaurant.query.filter(Restaurant.id == id).first()
    if not rest:
        return make_response({"error": "Restaurant not found"}, 404)
    if request.method == 'GET':
        return rest.to_dict(only=('id', 'name', 'address', 'pizzas', '-pizzas.restaurantpizza'))
    elif request.method == 'DELETE':
        db.session.delete(rest)
        db.session.commit()
        return make_response('', 201)

@app.route('/pizzas')
def pizzas():
    pizzas = Pizza.query.all()
    pizza_list = [pizza.to_dict(only=('id', 'name', 'ingredients')) for pizza in pizzas]
    return pizza_list

@app.route('/restaurant_pizzas', methods=['POST'])
def new_restaurant_pizza():
    req = request.get_json()
    try:
        new_rest_pizza = RestaurantPizza(
            price=req['price'],
            pizza_id=req['pizza_id'],
            restaurant_id=req['restaurant_id']
        )
    except ValueError:
        return make_response({"errors": ["validation errors"]}, 403)
    
    db.session.add(new_rest_pizza)
    db.session.commit()
    return Pizza.query.filter(Pizza.id==req['pizza_id']).first().to_dict(only=('id', 'name', 'ingredients'))

if __name__ == '__main__':
    app.run(port=5555, debug=True)
