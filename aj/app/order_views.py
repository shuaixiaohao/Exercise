
from datetime import datetime

from flask import Blueprint, render_template, url_for, \
    session, request, jsonify

from app.models import Order, House
from utils.check import is_login
from utils import status_code


order_blueprint = Blueprint('order', __name__)


@order_blueprint.route('/create_order/', methods=['POST'])
@is_login
def create_order():

    begin_date = datetime.strptime(request.form.get('begin_date'), '%Y-%m-%d')
    end_date = datetime.strptime(request.form.get('end_date'), '%Y-%m-%d')
    house_id = request.form.get('house_id')
    user_id = session['user_id']

    if not all([begin_date, end_date]):
        return jsonify(status_code.ORDER_BEGIN_END_DATA_NOT_NULL)

    if begin_date > end_date:
        return jsonify(status_code.ORDER_BEGIN_DATA_GT_END_DATE_ERROR)

    house = House.query.get(house_id)

    order = Order()
    order.user_id = user_id
    order.house_id = house_id
    order.begin_date = begin_date
    order.end_date = end_date
    order.days = (end_date - begin_date).days + 1
    order.house_price = house.price
    order.amount = order.days * order.house_price

    order.add_update()

    return jsonify(status_code.SUCCESS)

@order_blueprint.route('/orders/', methods=['GET'])
@is_login
def orders():
    return render_template('orders.html')


@order_blueprint.route('/allorders/', methods=['GET'])
def all_orders():
    u_id = session['user_id']
    order_list = Order.query.filter(Order.user_id == u_id).order_by(Order.id.desc()) # desc()降序
    order_list2 = [order.to_dict() for order in order_list]
    return jsonify(o_list=order_list2)

@order_blueprint.route('/lorders/', methods=['GET'])
def lorders():
    return render_template('lorders.html')

# 作为房东查询订单
@order_blueprint.route('/fd/', methods=['GET'])
def fd():
    # 查询当前用户的所有房屋编号
    u_id = session['user_id']
    house_list = House.query.filter(House.user_id==u_id)
    house_id_list = [house.id for house in house_list]
    # 根据房屋编号查找订单
    order_list = Order.query.filter(Order.house_id.in_(house_id_list)).order_by(Order.id.desc())
    # 构造结果
    o_list = [order.to_dict() for order in order_list]
    return jsonify(code=status_code.OK, o_list=o_list)

#修改订单状态
@order_blueprint.route('/order/<int:id>/', methods=['PUT'])
def status(id):
    # 接收参数：状态
    status = request.form.get('status')
    # 查找订单对象
    order = Order.query.get(id)
    # 修改
    order.status = status
    # 如果是拒单，需要添加原因
    if status == 'REJECTED':
        order.comment = request.form.get('comment')
    # 保存
    try:
        order.add_update()
    except:
        return jsonify(status_code.DATABASE_ERROR)

    return jsonify(code=status_code.OK)

