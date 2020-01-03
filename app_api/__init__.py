from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_marshmallow import Marshmallow
from flask_httpauth import HTTPDigestAuth


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'Путь до вашей БД'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['BUNDLE_ERRORS'] = False
app.config['SECRET_KEY'] = "Ваш Секретный Код"
auth = HTTPDigestAuth()
ma = Marshmallow(app)
db = SQLAlchemy(app)
api = Api(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


from app_api.routes import User, UserRegistration, ChangeUser, PostsMethods

api.add_resource(User, '/api/users')
api.add_resource(UserRegistration, '/api/new_user')
api.add_resource(ChangeUser, '/api/change_user')
api.add_resource(PostsMethods, '/api/posts')


if __name__ == '__main__':
    manager.run()
