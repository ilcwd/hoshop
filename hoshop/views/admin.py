# coding:utf8
"""

Author: ilcwd
"""

import flask

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
    r = shop.show_goods()
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

    r = shop.create_good(name, price, catalogid, total, description)
    if r.ok():
        pass

    return flask.redirect(flask.url_for('admin.add_good_view', error=u"添加商品成功"))


@app.route('/order/', methods=['GET', 'POST'])
@require_admin
def list_orders():
    cursor = flask.request.values.get('cursor', None)
    asc = int(flask.request.values.get('asc', 0))
    r = cart.sync_orders(cursor, limit=5, asc=asc)
    return flask.render_template('admin/orders.html',
                                 orders=r.data['orders'],
                                 forward_cursor=r.data.get('forward_cursor', ''),
                                 backward_cursor=r.data.get('backward_cursor', ''),
                                 latest_cursor=r.data.get('latest_cursor', ''),
                                 )
