from flask import Blueprint, request, jsonify
from helpers import token_required
from models import db, User, Guest, contact_schema, contacts_schema

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'yee': 'haw'}

@api.route('/guests', methods = ['POST'])
@token_required
def create_guest(current_user_token):
    name = request.json['name']
    email = request.json['email']
    phone_number = request.json['phone_number']
    address = request.json['address']
    RSVP = request.json['RSVP']
    meal = request.json['meal']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    guest = Guest(name, email, phone_number, address, RSVP, meal, user_token=user_token)

    db.session.add(guest)
    db.session.commit()

    response = contact_schema.dump(guest)
    return jsonify(response)

@api.route('/guests', methods = ['GET'])
@token_required
def get_guest(current_user_token):
    a_guest = current_user_token.token
    guests = Guest.query.filter_by(user_token = a_guest).all()
    response = contacts_schema.dump(guests)
    return jsonify(response)

@api.route('/guests/<id>', methods = ['GET'])
@token_required
def get_single_guest(current_user_token, id):
    guest = Guest.query.get(id)
    response = contact_schema.dump(guest)
    return jsonify(response)

@api.route('/guests/<id>', methods = ['POST', 'PUT'])
@token_required
def update_guest(current_user_token, id):
    guest = Guest.query.get(id)
    guest.name = request.json['name']
    guest.email = request.json['email']
    guest.phone_number = request.json['phone_number']
    guest.address = request.json['address']
    guest.RSVP = request.json['RSVP']
    guest.meal = request.json['meal']
    guest.user_token = current_user_token.token

    db.session.commit()
    response = contact_schema.dump(guest)
    return jsonify(response)

@api.route('/guests/<id>', methods = ['DELETE'])
@token_required
def delete_guest(current_user_token, id):
    guest = Guest.query.get(id)
    db.session.delete(guest)
    db.session.commit()
    response = contact_schema.dump(guest)
    return jsonify(response)
