
OK = 200
SUCCESS = {'code': 200, 'msg': '请求成功'}
DATABASE_ERROR = {'code': 0, 'msg': '数据不存在'}

# 用户模块
USER_REGISTER_DATA_NOT_NULL = {'code': '1001', 'msg': '请填写完整'}
USER_REGISTER_MOBILE_ERROR = {'code': '1002', 'msg': '手机号不正确'}
USER_REGISTER_PASSWORD_IS_NOT_VALID = {'code': '1003', 'msg': '密码不正确'}
USER_REGISTER_MOBILE_EXSITS = {'code': '1004', 'msg': '该用户已注册，请自接登录'}

USER_LOGIN_USER_NOT_EXSITS = {'code': '1004', 'msg': '该用户未注册'}
USER_REGISTER_PASSWORD_ERROR = {'code': '1005', 'msg': '用户名或密码错误'}

USER_CHANGE_PROFILE_IMAGES = {'code': '1006', 'msg': '头像修改失败'}
USER_CHANGE_PROFILE_IS_INVALID = {'code': '1007', 'msg': '用户名重复'}

USER_AUTH_NOT_EXSITS = {'code': '1008', 'msg': '请输入完整'}
USER_AUTH_ID_CARD_IS_NOT_VALID = {'code': '1009', 'msg': '请输入有效身份证号'}

# 订单模块
ORDER_BEGIN_END_DATA_NOT_NULL = {'code': '1100', 'msg': '入住时间不得为空'}
ORDER_BEGIN_DATA_GT_END_DATE_ERROR = {'code': '1101', 'msg': '离店时间不得提前于入住时间'}