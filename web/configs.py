import os
import traceback

from common import config
from flask import request
from flask import Blueprint

configs = Blueprint('configs', __name__)


@configs.route('/configs', methods=['GET'])
def config_list():
    config_dir = './configs'
    con_list = [os.path.splitext(f)[0] for f in os.listdir(config_dir) if f.endswith('.json')]
    return {'data': {'list': con_list}, 'code': 200}, 200


@configs.route('/configs/<string:con>/<string:fn>', methods=['GET'])
def config_detail(con, fn):
    data = config.load_ba_config(con)
    if fn not in data:
        return {'msg': '配置不存在', 'code': 500}, 500
    return {'data': data[fn], 'code': 200}, 200


@configs.route('/configs/<string:con>/<string:fn>', methods=['POST'])
def save_config(con, fn):
    data = config.load_ba_config(con)
    if fn not in data:
        return {'msg': '配置不存在', 'code': 500}, 500
    data[fn] = request.get_json()
    config.save_ba_config(con, data)
    return {'data': data[fn], 'code': 200}, 200


# 处理所有Exception类型的错误
@configs.errorhandler(Exception)
def handle_exception(e):
    full_traceback_info = traceback.format_exc()
    return {'msg': full_traceback_info, 'code': 500}, 500
