import traceback

from common import process
from common.baas import Baas
from flask import Blueprint, render_template

baas = Blueprint('baas', __name__, template_folder='templates')


@baas.route("/")
def homepage():
    return render_template('index.html')


@baas.route('/baas/start/<string:con>')
def start_baas(con):
    process.m.start_process(con)
    return {'data': {}, 'code': 200}, 200


@baas.route('/baas/stop/<string:con>')
def stop_baas(con):
    process.m.stop_process(con)
    return {'data': {}, 'code': 200}, 200


@baas.route('/baas/state/<string:con>')
def state_baas(con):
    return {'data': {'state': process.m.state_process(con)}, 'code': 200}, 200


@baas.route('/baas/schedule/<string:con>')
def schedule(con):
    running = process.m.state_process(con)
    return {'data': Baas(con).task_schedule(running), 'code': 200}, 200


# 处理所有Exception类型的错误
@baas.errorhandler(Exception)
def handle_exception(e):
    full_traceback_info = traceback.format_exc()
    return {'msg': full_traceback_info, 'code': 500}, 500
