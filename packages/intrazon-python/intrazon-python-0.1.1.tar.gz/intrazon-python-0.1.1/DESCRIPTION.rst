IntraZon Python SDK v. 0.1
==========================

IntraZon Python SDK allows you to use the IntraZon REST API without needing to handle the HTTPS transactions yourself.
It has two modes of operation: Blocking and non-blocking, which you select when creating the IntraZon object which
handles all the transactions. Blocking mode is simple: Any method which communicates with IntraZon will block until
the transaction has completely taken place, at which point it will return an object representing the result of the
transaction, or None in case of an error.

In non-blocking mode the methods will return immediately, and when the transaction is finished, a callback function
given by the user shall be called with the result; either the object describing the transaction, or an IntraZonError
object in case of an error. If non-blocking mode is used, the main thread should call stop() method on the IntraZon
object before exiting itself, or the thread in which IntraZon communications take place will continue to run. When
the SDK is used from a console program in this mode, it is recommended that an exit and keyboard interrupt handler which
calls stop() is implemented.

IntraZon Keys
=============

IntraZon uses a random, unique string as an identifier to all entity objects, such as players, applications and virtual
goods. This string is automatically assigned when the entity is created, and cannot be changed by the user. The keys can
be seen both with the IntraZon REST API, and in the IntraZon control panel to which all developers who connect their
applications to IntraZon will receive login credentials.

In addition, the identity of the REST API user is confirmed by providing a secret, 28 characters long key for each
IntraZon-enabled application. If this key is compromised, a new key can be requested in the control panel, which will
override the earlier key. The key can be seen in IntraZon control panel. It is placed in the back-end server, to confirm
its identity. It must be provided as the user name in the HTTP Basic authentication method, with empty password. Since
only HTTPS protocol is allowed for the IntraZon REST API, this is secure.

Example code
============

A simple example of the usage of IntraZon SDK can be seen by calling:

    python example.py listgoods aBcDeFgHiJ app_abcdefghijklmnopqrstuvwy

to receive a list of virtual goods and their keys for the given application (substitute app key and auth key with real
keys for your application). Then, to create a new player, register a credit card to it and make a purchase for one of
the virtual goods, call:

    python example.py newplayerpurchase aBcDeFgHiJ app_abcdefghijklmnopqrstuvwy 1234567890 "John Doe" 4012888888881881 
    123 12 2050
    
where, again, substitute the three example keys with real keys. Assuming the application is in test mode in the IntraZon
control panel, this transaction will succeed. The example credit card number above must be used for test transactions.
A real credit card must be used (note that it will be charged) if the application is not in test mode.

IntraZon entity classes
=======================

All IntraZon entities such as players, virtual goods are represented by classes which the SDK provides. They will have
the same attributes as the corresponding JSON object when the REST API is used directly. The currently supported
entities and their attributes are thus:

Application
-----------
 - key (string)
 - name (string)
 
VirtualGood
-----------
 - key (string)
 - name (string)
 - price (integer)
 - price_usd = (string; contains float)
 - price_eur = (string; contains float)
 - thumbnail = (string)
 - subscriber_discount = (string; contains float)
 - multiple = (boolean)
 - permanent = (boolean)
 
Player
------
 - key = (string)
 - name = (string)
 - subscribed = (boolean)
 - coins = (integer)
 - logged = (boolean)
 - last_login = (string)
 - app_unique_id = (string)
 
PaymentMethod
-------------
 - cc_num = (string, no spaces)
 - cc_csc = (string)
 - cc_name = (string)
 - cc_exp_month = (string, example "03")
 - cc_exp_year = (string, example "2050")
 
VirtualGoodPurchase
-------------------
 - virtual_good_key (string)
 - currency (string; "coins", "usd" or "eur")
 - amount (integer; 1 for any virtual goods which don't offer multiple purchases)
 
SDK methods
===========

virtual_goods(callback)
-----------------------
When communicating is done, calls the user-provided callback function with two arguments. In case of success, the first
argument is a list of VirtualGood objects, and the second is None. In case of error, the first argument is None and the
second is an IntraZonError object describing the error. Its code-field will correspond to the HTTP response code
received from IntraZon, if that was the cause of the error. If code is 599, a timeout happened, and if it is 1000 or
above, it was an internal error in the SDK in which case the message-field will contain information about it.

See: callb_list_virtual_goods(virtual_goods, error) in example.py for an example callback function.

add_player(self, callback, name)
--------------------------------
Similar to above, but the first argument given to the callback in case of success is just the one, created Player
object. See its key-field to see what key it was assigned and store it in your application. It is necessary to give a
name for the player. Rest of the optional arguments can be left out, in which case they will get default values

purchase_virtual_good(self, callback, player_key, virtual_good_key)
-------------------------------------------------------------------
Similarly to above, the first argument given to the callback in case of success is a VirtualGoodPurchase object
describing the given information, or None in case of error, and the second argument is the error, or None. This function
must be called with the player key of the player who does the purchase, and the Virtual Good key of the Virtual Good
being purchased.

register_payment_method(self, callback, player_key, cc_num, cc_csc, cc_name, cc_exp_month, cc_exp_year)
-------------------------------------------------------------------------------------------------------
Similarly to above, the first argument given to the callback in case of success is a PaymentMethod object describing the
payment method, or None in case of error, and the second argument is the error, or None. Key of the player whose payment
details are being registered must be provided, and the credit card details (without spaces): Number, CVC (security
code), name of the card holder (exactly as written on the credit card), expiration month as string with two digits
("03") and expiration year as string.

stop()
------
If IntraZon SDK is used in non-blocking mode, this must be called before exiting the program in order to stop the
communication thread.