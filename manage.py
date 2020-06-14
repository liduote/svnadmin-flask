from flask import jsonify
from flask_migrate import Migrate

from app import create_app
from app.extensions import db
from app.exception import InvalidUsage

app = create_app()
migrate = Migrate(app, db)


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
