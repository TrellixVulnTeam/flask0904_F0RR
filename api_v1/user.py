from flask import jsonify
from flask import request
from flask_jwt import jwt_required
from models import Fcuser, db
from . import api


@api.route('/users', methods=['GET','POST'])
@jwt_required()
def users():
    if request.method == 'POST':
        data = request.get_json()
        userid= data.get('userid')
        username= data.get('username')
        password= data.get('password')
        re_password= data.get('re-password')

        if not (userid and username and password and re_password):
            return jsonify({'error': 'No arguments'}), 400
        
        if password != re_password:
            return jsonify({'error': 'Wrong password'}), 400

        fcuser = Fcuser()
        fcuser.userid = userid
        fcuser.username = username
        fcuser.password = password

        db.session.add(fcuser)
        db.session.commit()

        return jsonify(), 201

    users = Fcuser.query.all()
    return jsonify([user.serialize for user in users])

@api.route('/users/<uid>', methods=['GET', 'PUT', 'DELETE'])
def user_detail(uid):
    if request.method == 'GET':
        user = Fcuser.query.filter(Fcuser.id == uid).first()
        return jsonify(user.serialize)
    elif request.method == 'DELETE':
        Fcuser.query.delete(Fcuser.id == uid)
        return jsonify(), 204

    data = request.get_json()

    Fcuser.query.filter(Fcuser.id == uid).update(data)
    user = Fccuser.query.filter(Fcuser.id == uid).first()
    return jsonify(user.serialize)