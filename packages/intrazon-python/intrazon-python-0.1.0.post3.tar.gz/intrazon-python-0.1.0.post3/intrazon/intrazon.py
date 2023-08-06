__author__ = 'mkoponen'
import json
from booby import Model, fields
from finch import Collection, Session
from tornado import httpclient, ioloop
from time import sleep
from threading import Thread
from errors import *


class Application(Model):
    key = fields.String()
    name = fields.String()

    def decode(self, response):
        return parse_application(json.loads(response.body))

    def __repr__(self):
        return 'Application({}/{})'.format(self.key, self.name)

def parse_application(raw):
    return {
        'key': raw['key'],
        'name': raw['name'],
    }


class VirtualGood(Model):
    key = fields.String()
    name = fields.String()
    price = fields.Integer()
    price_usd = fields.Float()
    price_eur = fields.Float()
    thumbnail = fields.String()
    subscriber_discount = fields.Float()
    multiple = fields.Boolean()
    permanent = fields.Boolean()

    def decode(self, response):
        return parse_virtual_good(json.loads(response.body))

    def __repr__(self):
        return 'VirtualGood({}/{})'.format(self.key, self.name)


class VirtualGoods(Collection):
    model = VirtualGood

    def __init__(self, application_key, *args, **kwargs):
        self.application_key = application_key

        super(VirtualGoods, self).__init__(*args, **kwargs)

    @property
    def url(self):
        return IntraZon.INTRAZON_API_URL_PREFIX + '/applications/{}/virtual-goods/'.format(self.application_key)

    def decode(self, response):
        return [parse_virtual_good(r) for r in json.loads(response.body)]


def parse_virtual_good(raw):
    return {
        'key': raw['key'],
        'name': raw['name'],
        'price': raw['price'],
        'thumbnail': raw['thumbnail'],
        'subscriber_discount': raw['subscriber_discount'],
    }


class VirtualGoodPurchase(Model):
    virtual_good_key = fields.String()
    currency = fields.String()
    amount = fields.Integer()

    def __init__(self, player_key, virtual_good_key, *args, **kwargs):
        self.virtual_good_key = virtual_good_key
        self.player_key = player_key
        super(VirtualGoodPurchase, self).__init__(*args, **kwargs)

    def decode(self, response):
        return parse_virtual_good_purchase(json.loads(response.body))

    def __repr__(self):
        return 'VirtualGoodPurchase({}/{})'.format(self.virtual_good_key, self.player_key)


class VirtualGoodPurchases(Collection):
    model = VirtualGoodPurchase

    def __init__(self, player_key, virtual_good_key, *args, **kwargs):
        self.player_key = player_key
        self.virtual_good_key = virtual_good_key

        super(VirtualGoodPurchases, self).__init__(*args, **kwargs)

    @property
    def url(self):
        return IntraZon.INTRAZON_API_URL_PREFIX + '/players/{}/buy-virtual-good/'.format(self.player_key)

    def decode(self, response):
        return [parse_virtual_good_purchase(r) for r in json.loads(response.body)]


def parse_virtual_good_purchase(raw):
    return {
        'currency': raw['currency'],
        'amount': raw['amount'],
    }


class Player(Model):
    key = fields.String()
    name = fields.String()
    subscribed = fields.Boolean()
    coins = fields.Integer()
    logged = fields.Boolean()
    last_login = fields.String()
    app_unique_id = fields.String()

    def __init__(self, application_key, *args, **kwargs):
        self.application_key = application_key
        super(Player, self).__init__(*args, **kwargs)

    def decode(self, response):
        return parse_player(json.loads(response.body))

    def __repr__(self):
        return 'Player({}/{})'.format(self.key, self.name)


class Players(Collection):
    model = Player

    def __init__(self, application_key, *args, **kwargs):
        self.application_key = application_key
        super(Players, self).__init__(*args, **kwargs)

    @property
    def url(self):
        return IntraZon.INTRAZON_API_URL_PREFIX + '/applications/{}/players/'.format(self.application_key)

    def decode(self, response):
        return [parse_player(r) for r in json.loads(response.body)]


def parse_player(raw):
    return {
        'key': raw['key'],
        'name': raw['name'],
        'subscribed': raw['subscribed'],
        'coins': raw['coins'],
        'logged': raw['logged'],
        'last_login': raw['last_login'],
        'app_unique_id': raw['app_unique_id'],
    }

class PaymentMethod(Model):
    cc_num = fields.String()
    cc_csc = fields.String()
    cc_name = fields.String()
    cc_exp_month = fields.String()
    cc_exp_year = fields.String()

    def __init__(self, player_key, *args, **kwargs):
        self.player_key = player_key
        super(PaymentMethod, self).__init__(*args, **kwargs)

    def decode(self, response):
        return parse_payment_method(json.loads(response.body))

    def __repr__(self):
        return 'PaymentMethod({}/{})'.format(self.cc_num, self.cc_name)


class PaymentMethods(Collection):
    model = PaymentMethod

    def __init__(self, player_key, *args, **kwargs):
        self.player_key = player_key

        super(PaymentMethods, self).__init__(*args, **kwargs)

    @property
    def url(self):
        return IntraZon.INTRAZON_API_URL_PREFIX + '/players/{}/payment-method/'.format(self.player_key)

    def decode(self, response):
        return [parse_payment_method(r) for r in json.loads(response.body)]


def parse_payment_method(raw):
    return {
        'cc_num': raw['cc_num'],
        'cc_csc': raw['cc_csc'],
        'cc_name': raw['cc_name'],
        'cc_exp_month': raw['cc_exp_month'],
        'cc_exp_year': raw['cc_exp_year'],
    }


class IntraZon(object):

    INTRAZON_DOMAIN = "https://iz.alpenwolf.com"
    INTRAZON_API_URL_PREFIX = INTRAZON_DOMAIN + "/api/v1"


    def __init__(self, application_key, auth_key, nonblocking=False):
        self.callback = None
        self.application_key = application_key
        self.auth_key = auth_key
        self.session = Session(httpclient.AsyncHTTPClient(), (auth_key, ""))
        self.nonblocking = nonblocking
        self.__last_returned_nonblocking_object = None
        if nonblocking is True:
            self.worker_thread = Thread(target=self.__tornado_ioloop_thread, args = ())
            self.worker_thread.start()

    def virtual_goods(self, callback):
        self.callback = callback
        virtual_goods = VirtualGoods(self.application_key, self.session)
        virtual_goods.all(self.__on_virtual_goods)
        if self.nonblocking is False:
            ioloop.IOLoop.instance().start()
            return self.__last_returned_nonblocking_object

    def add_player(self, callback, name, subscribed=False, coins=0, logged=False, last_login=None, app_unique_id=None):
        self.callback = callback
        new_player = Player(self.application_key)
        new_player.name = name
        new_player.subscribed = subscribed
        new_player.coins = coins
        new_player.logged = logged
        new_player.last_login = last_login
        new_player.app_unique_id = app_unique_id
        players = Players(self.application_key, self.session)
        players.add(new_player, self.__on_player_add)
        if self.nonblocking is False:
            ioloop.IOLoop.instance().start()
            return self.__last_returned_nonblocking_object

    def purchase_virtual_good(self, callback, player_key, virtual_good_key):
        self.callback = callback
        new_virtual_good_purchase = VirtualGoodPurchase(player_key, virtual_good_key)
        new_virtual_good_purchase.currency = "usd"
        new_virtual_good_purchase.amount = 1
        virtual_good_purchases = VirtualGoodPurchases(player_key, virtual_good_key, self.session)
        virtual_good_purchases.add(new_virtual_good_purchase, self.__on_virtual_good_purchase)
        if self.nonblocking is False:
            ioloop.IOLoop.instance().start()
            return self.__last_returned_nonblocking_object

    def register_payment_method(self, callback, player_key, cc_num, cc_csc, cc_name, cc_exp_month, cc_exp_year):
        self.callback = callback
        new_payment = PaymentMethod(player_key)
        new_payment.cc_num = cc_num
        new_payment.cc_csc = cc_csc
        new_payment.cc_name = cc_name
        new_payment.cc_exp_month = cc_exp_month
        new_payment.cc_exp_year = cc_exp_year
        payment_methods = PaymentMethods(player_key, self.session)
        payment_methods.add(new_payment, self.__on_payment_method_add)
        if self.nonblocking is False:
            ioloop.IOLoop.instance().start()
            return self.__last_returned_nonblocking_object

    def stop(self):
        if self.nonblocking is False:
            return

        ioloop.IOLoop.instance().stop()

    def __tornado_ioloop_thread(self):
        ioloop.IOLoop.instance().start()

    def __on_virtual_goods(self, virtual_goods, error):
        if error:
            if hasattr(error, "code"):
                iz_error = IntraZonError(error.code)
            else:
                print "Other exception: %s" % error.message
                iz_error = IntraZonError(1000)
            if self.nonblocking is False:
                self.__last_returned_nonblocking_object = None
                ioloop.IOLoop.instance().stop()
            self.callback(None, iz_error)
        else:
            if self.nonblocking is False:
                self.__last_returned_nonblocking_object = virtual_goods
                ioloop.IOLoop.instance().stop()
            self.callback(virtual_goods, None)

    def __on_player_add(self, player, error):
        if error:
            if hasattr(error, "code"):
                iz_error = IntraZonError(error.code)
            else:
                print "Other exception: %s" % error.message
                iz_error = IntraZonError(1000)
            if self.nonblocking is False:
                self.__last_returned_nonblocking_object = None
                ioloop.IOLoop.instance().stop()
            self.callback(None, iz_error)
        else:
            if self.nonblocking is False:
                self.__last_returned_nonblocking_object = player
                ioloop.IOLoop.instance().stop()
            self.callback(player, None)

    def __on_payment_method_add(self, payment_method, error):
        if error:
            if hasattr(error, "code"):
                iz_error = IntraZonError(error.code)
            else:
                print "Other exception: %s" % error.message
                iz_error = IntraZonError(1000)
            if self.nonblocking is False:
                self.__last_returned_nonblocking_object = None
                ioloop.IOLoop.instance().stop()
            self.callback(None, iz_error)
        else:
            if self.nonblocking is False:
                self.__last_returned_nonblocking_object = payment_method
                ioloop.IOLoop.instance().stop()
            self.callback(payment_method, None)

    def __on_virtual_good_purchase(self, virtual_good_purchase, error):
        if error:
            if hasattr(error, "code"):
                iz_error = IntraZonError(error.code)
            else:
                print "Other exception: %s" % error.message
                iz_error = IntraZonError(1000)
            if self.nonblocking is False:
                self.__last_returned_nonblocking_object = None
                ioloop.IOLoop.instance().stop()
            self.callback(None, iz_error)
        else:
            if self.nonblocking is False:
                self.__last_returned_nonblocking_object = virtual_good_purchase
                ioloop.IOLoop.instance().stop()
            self.callback(virtual_good_purchase, None)
