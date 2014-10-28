# coding:utf8
"""

Author: ilcwd
"""
import flask

from ..services import shop as _shop
from ..services import user as _user
from ..core import TEMPLATE_ROOT

app = flask.Blueprint('user', __name__, template_folder=TEMPLATE_ROOT)


@app.route('/info/', methods=['GET'])
def user_info():
    userid = flask.session['userid']
    cs = _shop.find_contacts(userid)

    u = _user.get_user(userid)

    return flask.render_template('user/info.html',
                                 contacts=cs.data['contacts'],
                                 default_contact=cs.data['default'],
                                 user=u.data)


@app.route('/contact/deletion', methods=['POST'])
def delete_contact():
    userid = flask.session['userid']
    contactid = flask.request.form['contactid']
    _shop.delete_contact(userid, contactid)
    return flask.redirect(flask.url_for('user.user_info'))


@app.route('/contact/setdefault', methods=['POST'])
def set_default_contact():
    userid = flask.session['userid']
    contactid = flask.request.form['contactid']
    _shop.set_primary_contact(userid, contactid)
    return flask.redirect(flask.url_for('user.user_info'))


@app.route('/login', methods=['GET'])
def login():
    next = flask.request.values.get('next', '')
    return flask.render_template('user/login.html', next=next)


@app.route('/logout', methods=['GET'])
def logout():
    flask.session.clear()
    return login()


@app.route('/login', methods=['POST'])
def login_do():
    loginid = flask.request.form['loginid']
    password = flask.request.form['password']
    logintype = flask.request.form['logintype']
    next = flask.request.values.get('next', '')

    r = _user.login(logintype, loginid, password)
    if not r.ok():
        return flask.render_template('user/login.html', next=next, error=r.error)

    flask.session['userid'] = r.data['userid']
    flask.session['user.role'] = r.data['role']
    if next:
        return flask.redirect(next)

    return flask.redirect(flask.url_for('user.user_info'))