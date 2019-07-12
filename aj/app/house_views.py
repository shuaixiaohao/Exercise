
import os

from flask import Blueprint, render_template, redirect, \
    url_for, request, jsonify, session

from app.models import Area, Facility, House, db, HouseImage, User
from utils import status_code
from utils.check import is_login
from utils.setting import UPLOAD_DIR

house_blueprint = Blueprint('house', __name__)

@house_blueprint.route('/myhouse/', methods=['GET'])
def myhouse():
    return render_template('myhouse.html')

@house_blueprint.route('/my_house/', methods=['GET'])
def my_house():
    houses = House.query.filter(House.user_id == session['user_id']).all()
    house_list = [house.to_dict() for house in houses]
    return jsonify(code=status_code.OK, houses=house_list)



@house_blueprint.route('/area_facility/')
def area_facility():
    areas = Area.query.all()
    facilitys = Facility.query.all()
    areas_list = [area.to_dict() for area in areas]
    facilitys_list = [facility.to_dict() for facility in facilitys]
    return jsonify(code=status_code.OK,
                   areas=areas_list,
                   facilitys=facilitys_list)


@house_blueprint.route('/newhouse/', methods=['GET', 'POST'])
def newhouse():
    if request.method == 'GET':
        return render_template('newhouse.html')
    if request.method == 'POST':
        data = request.form.to_dict()
        facility_ids = request.form.getlist('facility')

        house = House()
        house.user_id = session['user_id']
        house.area_id = data.get('area_id')
        house.title = data.get('title')
        house.price = data.get('price')
        house.address = data.get('address')
        house.room_count = data.get('room_count')
        house.acreage = data.get('acreage')
        house.beds = data.get('beds')
        house.unit = data.get('unit')
        house.capacity = data.get('capacity')
        house.deposit = data.get('deposit')
        house.min_days = data.get('min_days')
        house.max_days = data.get('max_days')

        facility_list = Facility.query.filter(Facility.id.in_(facility_ids)).all()
        house.facilities = facility_list
        try:
            house.add_update()
        except:
            db.session.rollback()
        return jsonify(code=status_code.OK, house_id=house.id)


@house_blueprint.route('/newhouse_image/', methods=['POST'])
def newhouse_image():
    # 接收房屋编号
    house_id = request.form.get('house_id')
    # 接收图片
    h_image = request.files.get('house_image')
    # 保存图片
    image_path = os.path.join(os.path.join(UPLOAD_DIR, 'house'), h_image.filename)
    h_image.save(image_path)

    # 保存到服务器
    image = HouseImage()
    image.house_id = house_id
    image.url = os.path.join('/static/upload/house', h_image.filename)
    image.add_update()

    # 房屋的默认图片
    house = House.query.get(house_id)
    if not house.index_image_url:
        house.index_image_url = os.path.join('/static/upload/house', h_image.filename)
        house.add_update()
    # 返回图片信息
    return jsonify(code=status_code.OK, url=image.url)


@house_blueprint.route('/detail/', methods=['GET'])
def detail():
    return render_template('detail.html')

@house_blueprint.route('/detail/<int:id>/', methods=['GET'])
def house_detail(id):
    house = House.query.get(id)
    house_info = house.to_full_dict()
    return jsonify(code=status_code.OK, house_info=house_info)


@house_blueprint.route('/booking/', methods=['GET'])
def booking():
    return render_template('booking.html')


@house_blueprint.route('/index/', methods=['GET'])
def index():
    return render_template('index.html')

@house_blueprint.route('/h_index/', methods=['GET'])
def h_index():
    user_name = ''
    if 'user_id' in session:
        user = User.query.filter(User.id==session['user_id']).first()
        user_name = user.name

    houses = House.query.order_by(House.id.desc()).all()
    houses_info = [house.to_dict() for house in houses]

    return jsonify(code=status_code.OK, user_name=user_name, houses_info=houses_info)
