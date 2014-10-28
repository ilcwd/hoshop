# coding:utf8
"""

Author: ilcwd
"""
import flask

from ..services import cart
from . import util


app = flask.Blueprint('ajax.cart', __name__)


@app.route('/cart/creation', methods=['GET', 'POST'])
def create_cart():
    r = cart.create_cart(0)
    if r.ok():
        return util.render_data(r.data)

    return util.render_error(u"创建购物车失败")


@app.route('/cart', methods=['GET', 'POST'])
def get_cart():
    cartid = flask.session['cartid']
    userid = flask.session['userid']
    r = cart.get_cart_details(userid, cartid)
    if r.ok():
        return util.render_data(r.data)

    return util.render_error(u"找不到购物车")


@app.route('/cart/deletegood', methods=['POST'])
def delete_good_from_cart():
    cartid = flask.session['cartid']
    userid = flask.session['userid']
    goodid = flask.request.form['goodid']
    r = cart.delete_good(userid, cartid, goodid)
    if r.ok():
        return util.render_data(r.data)

    return util.render_error(r.error)


@app.route('/cart/addgood', methods=['POST'])
def add_good_to_cart():
    cartid = flask.session['cartid']
    userid = flask.session['userid']
    goodid = flask.request.form['goodid']
    r = cart.add_good(userid, cartid, goodid)
    if r.ok():
        return util.render_data(r.data)

    return util.render_error(r.error)


@app.route('/order/sync', methods=['POST'])
def sync_orders():
    cursor = flask.request.form.get('cursor')
    limit = int(flask.request.form['limit'])
    asc = int(flask.request.form.get('asc'))
    r = cart.sync_orders(cursor, limit, asc)
    if r.ok():
        return util.render_data(r.data)

    return util.render_error(r.error)


@app.route('/order/update', methods=['POST'])
def update_order():
    userid = flask.session['userid']
    orderid = flask.request.form['orderid']
    status = flask.request.form['status']

    r = cart.update_order(userid, orderid, status, '')
    return util.render_dto(r)
