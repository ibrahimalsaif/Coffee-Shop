import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
#db_drop_and_create_all()

#---------------------------------------#
#       ROUTES                          #
#---------------------------------------#


@app.route('/drinks', methods=['GET'])
def get_drinks():

    drinks = Drink.query.all()

    if not drinks:
        abort(404)

    return jsonify({
        'success': True,
        'drinks': [drink.short() for drink in drinks]
    }), 200


@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def drinks_detail(token):

    drinks = Drink.query.all()

    if not drinks:
        abort(404)

    return jsonify({
        'success': True,
        'drinks': [drink.long() for drink in drinks]
    }), 200


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drinks(token):

    data = request.get_json()

    try:
        title = data.get('title', None)
        recipe = data.get('recipe', None)
        drink = Drink(title=title, recipe=json.dumps(recipe))
        drink.insert()

        the_drink = drink.long()

        return jsonify({
            'success': True,
            'drinks': the_drink
        }), 200

    except:
        abort(422)


@app.route('/drinks/<id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def edit_drinks(token, id):

    data = request.get_json()
    title = data.get('title', None)
    recipe = data.get('recipe', None)

    try:
        drink = Drink.query.filter_by(id=id).one_or_none()

        if not drink:
            abort(404)

        if title:
            drink.title = title

        if recipe:
            drink.recipe = json.dumps(recipe)

        drink.update()

        # updated_drink = Drink.query.filter(id=id).first()
        # the_drink = updated_drink.long()

        return jsonify({
            'success': True,
            'drinks': [drink.long()]
        }), 200

    except:
        abort(422)


@app.route('/drinks/<id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drinks(token, id):

    try:
        drink = Drink.query.filter_by(id=id).one_or_none()

        if not drink:
            abort(404)

        drink.delete()

        return jsonify({
            'success': True,
            'delete': id
        }), 200
    except:
        abort(422)

#---------------------------------------#
#       Error Handling                  #
#---------------------------------------#


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


@app.errorhandler(AuthError)
def not_found(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error['description']
    }), error.status_code
