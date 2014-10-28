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
    return flask.render_template('admin/add_good.html',
                                 catalogs=r.data['catalogs'])


@app.route('/good/addition', methods=['POST'])
@require_admin
def add_good_do():
    args = flask.request.form
    name = args['name']
    price = args['price']
    catalog = args['catalog']
    description = args['description']
    total = args['total']

    r = shop.create_good(name, price, catalog, total, description)
    if r.ok():
        pass

    return flask.redirect(flask.url_for('shop.list_goods'))


@app.route('/order/', methods=['GET', 'POST'])
@require_admin
def list_orders():
    r = cart.sync_orders(limit=10)
    return flask.render_template('admin/orders.html',
                                 orders=r.data['orders'],
                                 forward_cursor=r.data.get('forward_cursor', ''))
