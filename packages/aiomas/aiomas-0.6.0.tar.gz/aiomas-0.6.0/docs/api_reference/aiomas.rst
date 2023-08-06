.. module:: aiomas

``aiomas``
==========

This module provides easier access to the most used components of *aiomas*.
This purely for your convenience and you can, of cource, also import everything
from its actual submodule.

Decorators
----------

.. autosummary::
   ~aiomas.rpc.expose
   ~aiomas.codecs.serializable


Functions
---------

.. autosummary::
   ~aiomas.util.async
   ~aiomas.util.run
   ~aiomas.util.make_ssl_server_context
   ~aiomas.util.make_ssl_client_context


Exceptions
----------

.. autosummary::
   ~aiomas.exceptions.AiomasError
   ~aiomas.exceptions.RemoteException


Classes
-------

.. currentmodule:: aiomas.codecs
.. autosummary::
   ~aiomas.agent.Agent
   ~aiomas.agent.Container
   ~aiomas.agent.SSLCerts
   ~aiomas.codecs.JSON
   ~aiomas.codecs.MsgPack
   ~aiomas.codecs.MsgPackBlosc
   ~aiomas.clocks.AsyncioClock
   ~aiomas.clocks.ExternalClock
