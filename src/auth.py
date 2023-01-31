from flask import Blueprint, request, jsonify
import src.my_validators as validator
from wtforms import validators
from http import HTTPStatus
from src.dbmodels import User, db
from werkzeug.security import generate_password_hash, check_password_hash


auth = Blueprint(
    "auth",
    __name__,
    url_prefix="/api/auth"
)


@auth.post('/register')
def register():
    """
    Create a new user and store their information into the database.
    Register a user by receiving a POST request with the following parameters in the request body:

    Arguments: - request.json (dict): A dictionary containing the following keys:
    
        username (str): The username of the user to be registered.
        email (str): The email address of the user to be registered.
        password (str): The password of the user to be registered.

    Returns:
        dict: Returns a dictionary containing either a success message or an error message with an HTTP status code.
        In case of success:
            - 'message': 'User created'
            - 'user':
                - 'username': The username of the new user
                - 'email': The email of the new user
                
        In case of failure:
        - tuple: If there is an error, returns a tuple of a dictionary containing the error message and an HTTP status code. The dictionary will have the following format:
            - 'error': error message (str)
            - HTTP status code: 
                - HTTPStatus.BAD_REQUEST (400): If the validation of the username or password failed.
                - HTTPStatus.CONFLICT (409): If the email or username is already taken.
                
                
            {'error': 'username taken'}, HTTPStatus.CONFLICT
            {'error': 'check your email'}, HTTPStatus.BAD_REQUEST
            {'error': password_res['message']}, HTTPStatus.BAD_REQUEST
            {'error': username_res['message']}, HTTPStatus.BAD_REQUEST
        
    """
    
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    
    
    username_res =validator.my_username_validator(username=username)
    if not username_res['status']:
        return jsonify({'error': username_res['message']}), HTTPStatus.BAD_REQUEST

    password_res = validator.my_password_validator(password=password)
    if not password_res['status']:
        return jsonify({'error': password_res['message']}), HTTPStatus.BAD_REQUEST
    
    if not validators.email(email):
        return jsonify({'error': 'check your email'}), HTTPStatus.BAD_REQUEST

    if User.query.filter_by(email=email).first() is not None:
        return jsonify({'error': 'email taken'}), HTTPStatus.CONFLICT
    
    if User.query.filter_by(username=username).first() is not None:
        return jsonify({'error': 'username taken'}), HTTPStatus.CONFLICT
    
    
    pwd_hash =generate_password_hash(password)
    print(username)
    print(pwd_hash)
    print(email)
    user = User(password=pwd_hash, username=username, email=email)
    db.session.add(user)
    db.session.commit()
    
    
    return jsonify({
        'message':'User created',
        'user':{
            'username':username,
            'email':email
        }
        }), HTTPStatus.CREATED


@auth.get('/user')
def user():
    return {'user': 'Ilonze Chukwunonso'}
