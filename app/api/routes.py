from flask import Blueprint, request, jsonify
from helpers import token_required
from models import db, User, Song, contact_schema, contacts_schema

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'yee': 'haw'}

@api.route('/songs', methods = ['POST'])
@token_required
def create_song(current_user_token):
    title = request.json['title']
    artist = request.json['artist']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    song = Song(title, artist, user_token=user_token)

    db.session.add(song)
    db.session.commit()

    response = contact_schema.dump(song)
    return jsonify(response)

@api.route('/songs', methods = ['GET'])
@token_required
def get_song(current_user_token):
    a_song = current_user_token.token
    songs = Song.query.filter_by(user_token = a_song).all()
    response = contacts_schema.dump(songs)
    return jsonify(response)

@api.route('/songs/<id>', methods = ['GET'])
@token_required
def get_single_song(current_user_token, id):
    song = Song.query.get(id)
    response = contact_schema.dump(song)
    return jsonify(response)

@api.route('/songs/<id>', methods = ['POST', 'PUT'])
@token_required
def update_song(current_user_token, id):
    song = Song.query.get(id)
    song.title = request.json['title']
    song.artist = request.json['artist']
    song.user_token = current_user_token.token

    db.session.commit()
    response = contact_schema.dump(song)
    return jsonify(response)

@api.route('/songs/<id>', methods = ['DELETE'])
@token_required
def delete_song(current_user_token, id):
    song = Song.query.get(id)
    db.session.delete(song)
    db.session.commit()
    response = contact_schema.dump(song)
    return jsonify(response)
