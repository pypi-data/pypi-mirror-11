===============================
GrandCentral
===============================

.. image:: https://img.shields.io/pypi/v/grandcentral.svg
        :target: https://pypi.python.org/pypi/grandcentral-py


GrandCentral is an extremely basic publisher subscriber event library

* Free software: ISC license
* Documentation: https://grandcentral.readthedocs.org.

Description
-----------

GrandCentral is an extremely basic publisher subscriber event library. It provides only
two methods

a) publish:- it publishes an event on provided channel with a payload

b) subscribe:- it registers channel/event pair with a consumer that is to be called when that particular event is published on the channel.


GrandCentralConsumer is an abstract class that determines how an event emitted
by grandcentral is to be handled. Currently the library provides two simple consumers

a) SyncConsumer which receives a callable and executes that callable synchronously

b) CeleryConsumer which receives a celery task and execute that asynchornously using celery.

A library also provides a DjangoCentral which also allows to subscribe to built in
django signals like pre-save, post-save, pre-delete, post-delete etc.

