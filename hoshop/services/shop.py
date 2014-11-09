# coding:utf8
"""

Author: ilcwd
"""
import datetime

from ..models import (
    catalog as _catalog,
    good as _good,
    contact as _contact,
)
from hoshop.core import misc

from .dtos import HoShopDTO


def find_catalogs():
    return HoShopDTO(data=dict(
        catalogs=_catalog.find_catalogs(),
    ))


def create_catalog(name):
    catalog = _catalog.create_catalog(name)
    if catalog is not None:
        return HoShopDTO(data=catalog.dictify())

    return HoShopDTO(error='create catalog fail')


def show_goods():
    catalogs = _catalog.find_catalogs()
    goods = _good.find_goods()

    return HoShopDTO(data=dict(
        catalogs=catalogs,
        goods=goods,
    ))


def update_goods(goodid, **kw):
    if 'price' in kw:
        kw['price'] = misc.encode_price(kw.pop('price'))
    if 'expired_time' in kw:
        kw['expired_time'] = datetime.datetime.strptime(kw.pop('expired_time'), '%Y-%m-%d')

    if _good.update_good(goodid, **kw):
        return HoShopDTO()

    return HoShopDTO(error=u'更新商品失败')


def get_primary_contact(userid):
    c = _contact.get_default_contact(userid)
    if c:
        return HoShopDTO(data=c)
    return HoShopDTO(error="not found")


def set_primary_contact(userid, contactid):
    c = _contact.get_contact(contactid)
    if not c:
        return HoShopDTO(error="contact not found")

    ok = _contact.set_default_contact(userid, contactid) == 1
    if ok:
        return HoShopDTO()

    return HoShopDTO(error="set primary contact fail")


def find_contacts(userid):
    cs = _contact.find_contacts(userid)
    r = {'contacts': cs, 'default': None}
    if cs:
        r['default'] = _contact.get_default_contact(userid)
    return HoShopDTO(data=r)


def delete_contact(userid, contactid):
    if _contact.delete_contact(userid, contactid):
        return HoShopDTO()

    return HoShopDTO(error='delete contact fail')


def create_good(name, price, catalogid, total=99999999, description='', start_time=None, expired_time=None):
    price = misc.encode_price(price)
    c = _catalog.get_catalog(catalogid);
    rows = _good.create_good(name, price, catalogid, total, description, start_time, expired_time)

    if rows == 1:
        return HoShopDTO(data='')

    return HoShopDTO(error='create good fail')