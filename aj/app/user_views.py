import re
import os

from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session

from app.models import User, db
from utils import status_code
from utils.check import is_login
from utils.setting import UPLOAD_DIR

user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/')
def aaa():
    return '你好'

@user_blueprint.route('/create_db/')
def create_db():
    db.create_all()
    return '创建成功'

@user_blueprint.route('/register/', methods=['GET'])
def register():
        return render_template('register.html')

@user_blueprint.route('/register/', methods=['POST'])
def user_register():
        mobile = request.form.get('mobile')
        pwd = request.form.get('password')
        pwd2 = request.form.get('password2')
        if not all([mobile, pwd, pwd2]):
            return jsonify(status_code.USER_REGISTER_DATA_NOT_NULL)
        # 验证手机号正确性
        if not re.match(r'^1[34578]\d{9}$', mobile):
            return jsonify(status_code.USER_REGISTER_MOBILE_ERROR)
        if pwd != pwd2:
            return jsonify(status_code.USER_REGISTER_PASSWORD_IS_NOT_VALID)
        # 保存用户数据
        user = User.query.filter(User.phone==mobile).first()
        if user:
            return jsonify(status_code.USER_REGISTER_MOBILE_EXSITS)
        else:
            user = User()
            user.phone = mobile
            user.password = pwd
            user.name = mobile
            user.add_update()
            return jsonify(status_code.SUCCESS)



@user_blueprint.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        mobile = request.form.get('mobile')
        password = request.form.get('password')

        if not all([mobile, password]):
            return jsonify(status_code.USER_REGISTER_DATA_NOT_NULL)
        # 验证手机号正确性
        if not re.match(r'^1[34578]\d{9}$', mobile):
            return jsonify(status_code.USER_REGISTER_MOBILE_ERROR)
        # 验证用户
        user = User.query.filter(User.phone == mobile).first()
        if user:
            if user.check_pwd(password):
                session['user_id'] = user.id
                return jsonify(status_code.SUCCESS)
            else:
                return jsonify(status_code.USER_REGISTER_PASSWORD_ERROR)
        else:
            return jsonify(status_code.USER_LOGIN_USER_NOT_EXSITS)


@user_blueprint.route('/my/', methods=['GET'])
@is_login
def my():
        return render_template('my.html')



@user_blueprint.route('/profile/', methods=['GET', 'PATCH'])
@is_login
def profile():
    if request.method == 'GET':
        return render_template('profile.html')
    if request.method == 'PATCH':
        file = request.files.get('avatar')
        # 校验上传图片格式正确性
        if not re.match(r'image/.*', file.mimetype):
            return jsonify(status_code.USER_CHANGE_PROFILE_IMAGES)
        # 保存
        image_path = os.path.join(UPLOAD_DIR, file.filename)
        file.save(image_path)

        user = User.query.get(session['user_id'])
        avatar_path = os.path.join('upload', file.filename)
        user.avatar = avatar_path
        try :
            user.add_update()
        except Exception as e:
            db.session.rollback()
            return jsonify(status_code.DATABASE_ERROR)
        return jsonify(code=status_code.OK, image_url=avatar_path)

@user_blueprint.route('/proname/', methods=['PATCH'])
@is_login
def proname():
    name = request.form.get('name')
    user = User.query.filter_by(name=name).first()
    if user:
        return jsonify(status_code.USER_CHANGE_PROFILE_IS_INVALID)
    else:
        user = User.query.get(session['user_id'])
        user.name = name
        try:
            user.add_update()
        except:
            db.session.rollback()
            return jsonify(status_code.DATABASE_ERROR)
        return jsonify(code=status_code.OK, name=name)

@user_blueprint.route('/user/', methods=['GET', 'POST'])
@is_login
def user_info():
    user = User.query.get(session['user_id'])
    return jsonify(code=status_code.OK, data=user.to_basic_dict())


@user_blueprint.route('/auth/', methods=['GET'])
@is_login
def get_auth():
    return render_template('auth.html')


@user_blueprint.route('/auth/', methods=['GET'])
@is_login
def auth():
    user = User.query.get(session['user_id'])
    return jsonify(code=status_code.ok, data=user.to_basic_dict())


@user_blueprint.route('/auth/', methods=['PATCH'])
@is_login
def user_auth():
    id_name = request.form.get('real_name')
    id_card = request.form.get('id_card')
    user = User.query.get(session['user_id'])
    if not all([id_name, id_card]):
        return jsonify(status_code.USER_AUTH_NOT_EXSITS)
    if not re.match(r'^[1-9]\d{17}$', id_card):
        return jsonify(status_code.USER_AUTH_ID_CARD_IS_NOT_VALID)

    user.id_name = id_name
    user.id_card = id_card
    try:
        user.add_update()
    except:
        db.session.rollback()
        return jsonify(status_code.DATABASE_ERROR)
    return jsonify(status_code.SUCCESS)


@user_blueprint.route('/auths/', methods=['GET'])
@is_login
def user_auths():
    user = User.query.get(session['user_id'])
    return jsonify(code=status_code.OK, data=user.to_auth_dict())