#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood
from sqlalchemy.orm import joinedload

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = Bakery.query.all()
    bakery_list = []
    
    for bakery in bakeries:
        bakery_data = {
            "baked_goods": [],
            "created_at": bakery.created_at,
            "id": bakery.id,
            "name": bakery.name,
            "updated_at": bakery.updated_at,
            }
        
        for baked_good in bakery.baked_goods:
            good_data = {
                "id": baked_good.id,
                'bakery_id': baked_good.bakery_id,
                'name': baked_good.name,
                'price': float(baked_good.price),
                "created_at": baked_good.created_at,
                "updated_at": baked_good.updated_at,
            }
            bakery_data["baked_goods"].append(good_data)
        bakery_list.append(bakery_data)

    response = make_response(jsonify(bakery_list))
    response.headers['Content-Type'] = 'application/json'

    return response

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter_by(id=id).first()
    if bakery:
        bakery_data = {
            "baked_goods": [],
            "created_at": bakery.created_at,
            "id": bakery.id,
            "name": bakery.name,
            "updated_at": bakery.updated_at,
            }
        
        for baked_good in bakery.baked_goods:
            good_data = {
                "bakery_id": baked_good.bakery_id,
                "created_at": baked_good.created_at,
                'id': baked_good.id,
                'name': baked_good.name,
                'price': float(baked_good.price),
                "updated_at": baked_good.updated_at,
            }
            bakery_data["baked_goods"].append(good_data)

    response = make_response(jsonify(bakery_data))
    response.headers['Content-Type'] = 'application/json'
    
    return response

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = BakedGood.query.options(joinedload(BakedGood.bakery)).order_by(BakedGood.price.desc()).all()
    baked_goods_list = []
    for good in baked_goods:
        good_data = {
            "bakery": {
                "created_at": good.bakery.created_at,
                "id": good.bakery.id,
                "name": good.bakery.name,
                "updated_at": good.bakery.updated_at
            } if good.bakery else None,
            "bakery_id": good.bakery_id,
            "created_at": good.created_at,
            "id": good.id,
            "name": good.name,
            "price": good.price,
            "updated_at": good.updated_at
        }
        baked_goods_list.append(good_data)  

    response = jsonify(baked_goods_list)
    response.headers['Content-Type'] = 'application/json'
    
    return response

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    expensive_good = BakedGood.query.options(joinedload(BakedGood.bakery)).order_by(BakedGood.price.desc()).first()
    if expensive_good and expensive_good.bakery: 
        expensive_good_data = {
            'bakery': {
                "created_at": expensive_good.bakery.created_at,
                "id": expensive_good.bakery.id,
                "name": expensive_good.bakery.name,
                "updated_at": expensive_good.bakery.updated_at
            },
            "bakery_id": expensive_good.bakery_id,
            "created_at": expensive_good.created_at,
            'id': str(expensive_good.id),
            "name": expensive_good.name,
            'price': str(expensive_good.price),
            "updated_at": expensive_good.updated_at
        }
    else: 
        expensive_good_data = {
            "id": None,
            "name": None,
            "price": None,
        }
    
    response = make_response(jsonify(expensive_good_data))
    response.headers['Content-Type'] = 'application/json'
        
    return response
    
if __name__ == '__main__':
    app.run(port=5555, debug=True)
