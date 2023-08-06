Overview
========

Aiomas' main goal is making it easier to create distributed systems (like
multi-agent systems (MAS)) with pure Python and `asyncio`__.

Therefore, it adds three layers of abstraction around the transports (TCP or
Unix domain sockets) that asyncio provides:

__ https://docs.python.org/3/library/asyncio.html

.. image:: /_static/overview.*
   :width: 430
   :align: center
   :alt: The three architectual layers of aiomas


1. The :doc:`channel layer <channel>` allows you to send and receive actual
   data like strings, lists ob numbers instead of single bytes.

   The :class:`~aiomas.channel.Channel` class lets you make *requests* and wait
   for the corresponding *replies* within a coroutine__: ``reply = await
   channel.send(request)``.

   Every *channel* has a :class:`~aiomas.codecs.Codec` instance that is
   responsible for (de)serializing the data that is being sent via the channel.
   By default, JSON__ is used for that.  Alternatively, you can use MsgPack__
   and optionally compress it using Blosc__.  You can also extend codecs with
   custom serializers for more object types.

__ https://docs.python.org/3/library/asyncio-task.html#coroutine
__ http://www.json.org/
__ http://msgpack.org/
__ http://blosc.org/

2. The :doc:`remote procedure call (RPC) layer <rpc>` lets you call function on
   remote objects.

   You can expose the methods of an object as well as functions within a dict.
   On the other side of the connection, proxy objects represent these exposed
   functions.

   You can call remote functions within a coroutine: ``return_value = await
   remote.method('spam', eggs=3.14)``.

3. The :doc:`agent layer <agent>` hides some of the *RPC* layer's complexity
   and allows you to create thousands of interconnected objects *(agents)*
   without opening thousands of unique connections between them.

   Therefore, all agents live within a *container*.  Containers take care of
   creating agent instances and performing the communication between them.

   The container provides a *clock* for the agents. This clock can either be
   synchronized with the real (wall-clock) time or be set by an external
   process (e.g., other simulators).

The following sections explain theses layers in more detail.
