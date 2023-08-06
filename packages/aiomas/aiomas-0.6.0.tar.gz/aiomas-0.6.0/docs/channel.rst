The channel layer
=================

Here is a minimal example that shows how the :class:`~aiomas.channel.Channel`
can be used:

.. code-block:: python

   >>> import aiomas
   >>>
   >>>
   >>> ADDR = ('localhost', 5555)
   >>>
   >>>
   >>> async def handle_client(channel):
   ...    req = await channel.recv()
   ...    print(req.content)
   ...    await req.reply('cya')
   ...    channel.close()
   >>>
   >>>
   >>> async def client():
   ...    channel = await aiomas.channel.open_connection(ADDR)
   ...    rep = await channel.send('ohai')
   ...    print(rep)
   ...    channel.close()
   >>>
   >>>
   >>> server = aiomas.run(aiomas.channel.start_server(ADDR, handle_client))
   >>> aiomas.run(client())
   ohai
   cya
   >>> server.close()
   >>> aiomas.run(server.wait_closed())


How can I bind a server socket to a random port?
------------------------------------------------

You cannot ask your OS for an available port but have to try a randomly chosen
port until you succeed:

.. code-block:: python

   >>> import random
   >>>
   >>> max_tries = 100
   >>> port_range = (49152, 65536)
   >>>
   >>> async def random_server(host, port_range, max_tries):
   ...     for i in range(max_tries):
   ...         try:
   ...             port = random.randrange(*port_range)
   ...             server = await aiomas.channel.start_server(
   ...                (host, port), handle_client)
   ...         except OSError as oe:
   ...             if oe.errno != 48:
   ...                 # Re-raise if not errno 48 ("address already in use")
   ...                 raise
   ...         else:
   ...             return server, port
   ...     raise RuntimeError('Could not bind server to a random port.')
   >>>
   >>> server, port = aiomas.run(random_server('localhost', port_range, max_tries))
   >>> server.close()
   >>> aiomas.run(server.wait_closed())
