#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, make_response
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route("/")
def index():
    return "<h1>Code challenge</h1>"

@app.route("/restaurants", methods=["GET"])
def get_restaurants():
    restaurants = Restaurant.query.all()
    return [r.to_dict(only=("id", "name", "address")) for r in restaurants], 200

@app.route('/restaurants/<int:id>')
def get_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if restaurant:
        return restaurant.to_dict(), 200
    return {"error": "Restaurant not found"}, 404

@app.route('/restaurants/<int:id>', methods=['DELETE'])
def delete_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if not restaurant:
        return {"error": "Restaurant not found"}, 404
    db.session.delete(restaurant)
    db.session.commit()
    return '', 204


@app.route('/pizzas')
def get_pizzas():
    return [p.to_dict(only=('id', 'name', 'ingredients')) for p in Pizza.query.all()], 200


@app.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    data = request.get_json()
    try:
        rp = RestaurantPizza(
            price=data['price'],
            pizza_id=data['pizza_id'],
            restaurant_id=data['restaurant_id']
        )
        db.session.add(rp)
        db.session.commit()
        return rp.to_dict(), 201
    except Exception as e:
        return {"errors": [str(e)]}, 400




if __name__ == "__main__":
    app.run(port=5555, debug=True)
