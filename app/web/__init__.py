from flask import Blueprint

main = Blueprint('main', __name__, url_prefix='')

from .project import *
from .login import *
from app.web.admin import *
