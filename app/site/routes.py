from flask import Blueprint

site = Blueprint('site', __name__)

@site.route('/')
def home():
    return 'Home'

@site.route('/profile')
def profile():
    return 'Profile'