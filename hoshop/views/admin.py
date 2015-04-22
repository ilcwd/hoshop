# coding:utf8
"""

Author: ilcwd
"""

import flask

from ..biz import workinghour
from ..services import shop, cart
from ..core import TEMPLATE_ROOT
from .default import require_admin

app = flask.Blueprint('admin', __name__, template_folder=TEMPLATE_ROOT)


@app.route('/good/addition', methods=['GET'])
@require_admin
def add_good_view():
    r = shop.find_catalogs()
    error = flask.request.values.get('error', '')
    return flask.render_template('admin/add_good.html',
                                 catalogs=r.data['catalogs'], error=error)


@app.route('/good/update')
@require_admin
def update_good():
    r = shop.show_goods(show_zero_goods=True)
    return flask.render_template('admin/update_good.html', goods=r.data['goods'], catalogs=r.data['catalogs'])


@app.route('/good/addition', methods=['POST'])
@require_admin
def add_good_do():
    args = flask.request.form
    name = args['name']
    price = args['price']
    catalogid = args['catalogid']
    description = args['description']
    total = args['total']
    photos = args['photos']

    if photos:
        photos = filter(None, photos.split(','))

    print args
    r = shop.create_good(name, price, catalogid, total, description, photos=photos)
    if r.ok():
        pass

    return flask.redirect(flask.url_for('admin.add_good_view', error=u"添加商品成功"))


@app.route('/order/', methods=['GET', 'POST'])
@require_admin
def list_orders():
    cursor = flask.request.values.get('cursor', None)
    asc = int(flask.request.values.get('asc', 0))
    r = cart.sync_orders(cursor, limit=10, asc=asc)
    return flask.render_template('admin/orders.html',
                                 orders=r.data['orders'],
                                 forward_cursor=r.data.get('forward_cursor', ''),
                                 backward_cursor=r.data.get('backward_cursor', ''),
                                 latest_cursor=r.data.get('latest_cursor', ''),
                                 )


@app.route('/workinghour', methods=['GET'])
@require_admin
def show_workinghour():
    msg = workinghour.is_rest_time()
    return flask.render_template('admin/workingtime.html', msg=msg)


@app.route('/workinghour/addition', methods=['POST'])
@require_admin
def add_workinghour():
    st = flask.request.form['start_time']
    workinghour.create_working_hour(start_time=st, msg=u'小店休息中，营业开始时间：%(start_time)s')
    return flask.redirect(flask.url_for('admin.show_workinghour'))