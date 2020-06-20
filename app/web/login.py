import json

from . import main
from app.model import User


@main.route('/login', methods=['POST'])
def login():
    return 'admin'


@main.route('/get_info', methods=['GET'])
def get_info():
    user = {
        'name': 'super_admin',
        'user_id': '1',
        'access': ['super_admin', 'admin'],
        'token': 'super_admin',
        'avatar': 'https://file.iviewui.com/dist/a0e88e83800f138b94d2414621bd9704.png'
    }
    return json.dumps(user)
