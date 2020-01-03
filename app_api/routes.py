import re
from flask_restful import Resource, reqparse
from app_api import ma, db, api, auth
from app_api.models import Users, Posts

# ----------------------UserSchema---------------------------------------------------#


class UserSchema(ma.Schema):
    class Meta():
        fields = ("username", "email")


user_schema = UserSchema()
users_schema = UserSchema(many=True)

# ----------------------PostSchema---------------------------------------------------#


class PostSchema(ma.Schema):
    class Meta():
        fields = ("title", "post_body", "author")


post_schema = PostSchema()
posts_schema = PostSchema(many=True)

regex_email = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
regex_password = '[A-Za-z0-9@#$%^&+=]{8,}'
unvalid_password_message = "At least 8 characters Must be restricted to, though does not specifically require any of: \n uppercase letters: A-Z \nI lowercase letters: a-z \nI numbers: 0-9\nI any of the special characters: @#$%^&+="



parser = reqparse.RequestParser(bundle_errors=True)   # main parser

@auth.get_password
def get_pw(username):
    user = Users.query.filter_by(username=username).first()
    if  user:
        return user.password
    return None


class User(Resource):
    """Получение списка всех пользователей"""
    @auth.login_required
    def get(self):
        user = Users.query.all()
        return users_schema.dump(user)


class UserRegistration(Resource):
    def get(self):
        return "Via POST method you can register!"

    def post(self):
        parser.add_argument('username', type=str, help='Bad')
        parser.add_argument('password', type=str)
        parser.add_argument('email', type=str)
        args = parser.parse_args()
        username_chek = Users.query.filter_by(username=args['username']).first()
        email_chek = Users.query.filter_by(email=args['email']).first()
        valid_email = re.search(regex_email, args['email'])
        valid_password = re.search(regex_password, args['password'])
        if username_chek or email_chek:
            return 'Thats account already exist'
        elif len(args['username']) < 3:
            return 'Minimu 3 character'
        elif not valid_password:
            return unvalid_password_message
        elif not valid_email:
            return 'Please input correct email'
        else:
            new_user = Users(username=args['username'], password=args
                                            ['password'], email=args['email'])
            db.session.add(new_user)
            db.session.commit()
            return 'Registration complite!'
    

class ChangeUser(Resource):
    @auth.login_required
    def delete(self):
        user = Users.query.filter_by(username=auth.username()).first()
        parser.add_argument('username', type=str)
        args = parser.parse_args()
        delete_user = Users.query.filter_by(username=args['username']).first()
        if user.permission != "Admin":
            return "You have not permission for this!"
        elif not delete_user:
            return f"User with username - {args['username']} does not exist!"
        else:
            db.session.delete(delete_user)
            db.session.commit()
            return f"User with username {args['username']} was deleted"
    @auth.login_required
    def put(self):
        user = Users.query.filter_by(username=auth.username()).first()
        parser.add_argument('username', type=str)
        parser.add_argument('email', type=str)
        args = parser.parse_args()
        if not args['email']:
            user.username = args['username']
            db.session.commit()
            return 'Your username updated'
        elif not args['username']:
            user.email = args['email']
            db.session.commit()
            return 'Your email updated'
        else:
            user.username = args['username']
            user.email = args['email']
            db.session.commit()
            return "Your accoiunt updated"
        

class PostsMethods(Resource):
    @auth.login_required
    def get(self):
        all_posts = Posts.query.all()
        return posts_schema.dump(all_posts)
    
    @auth.login_required
    def post(self):
        parser.add_argument('title', type=str)
        parser.add_argument('post_body', type=str)
        args = parser.parse_args()
        new_post = Posts(title=args['title'], post_body=args['post_body'], author=auth.username())
        db.session.add(new_post)
        db.session.commit()
        return 'New Post Add'
        

