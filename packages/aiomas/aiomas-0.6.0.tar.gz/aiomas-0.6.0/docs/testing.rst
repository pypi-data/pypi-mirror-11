Testing and debugging
=====================

*[Status: draft]*

- asyncio's debug mode is honored.  If it is activate, aiomas also falls into
  debug mode and gives you better / more detailed exceptions in some cases.
  This impacts performance, so it isn't activated always.


Testing coroutines with pytest
------------------------------

A naïve approach would be:

.. code-block:: python

   # tests/test_coros.py
   import asyncio

   def test_coro():
       loop = asyncio.get_event_loop()

       async def do_test():
           await asyncio.sleep(0.1)
           assert 0  # onoes!

       loop.run_until_complete(do_test())


Creating and closing a loop should better be a fixture:

.. code-block:: python

   # tests/conftest.py
   import asyncio


   @pytest.yield_fixture
   def loop():
       loop = asyncio.new_event_loop()
       asyncio.set_event_loop(loop)
       yield loop
       loop.close()


   # tests/test_coros.py
   def test_coro(loop):
       async def do_test():
           await asyncio.sleep(0.1)
           assert 0  # onoes!

       loop.run_until_complete(do_test())


Wouldn't it be cool if tests actually looked like this:

.. code-block:: python

   # tests/test_coros.py
   async def test_coro(loop):
       await asyncio.sleep(0.1)
       assert 0


It's possible. You just have to create a small pytest plug-in:

.. code-block:: python

   # tests/conftest.py
   import asyncio


   @pytest.yield_fixture
   def loop():
       loop = asyncio.new_event_loop()
       asyncio.set_event_loop(loop)
       yield loop
       loop.close()


   def pytest_pycollect_makeitem(collector, name, obj):
       """Collect asyncio coroutines as normal functions, not as generators."""
       if collector.funcnamefilter(name) and asyncio.iscoroutinefunction(obj):
           return list(collector._genfunctions(name, obj))


   def pytest_pyfunc_call(pyfuncitem):
       """If ``pyfuncitem.obj`` is an asyncio coroutinefunction, execute it via
       the event loop instead of calling it directly."""
       testfunction = pyfuncitem.obj

       if not asyncio.iscoroutinefunction(testfunction):
           return

       # Copied from _pytest/python.py:pytest_pyfunc_call()
       funcargs = pyfuncitem.funcargs
       testargs = {}
       for arg in pyfuncitem._fixtureinfo.argnames:
           testargs[arg] = funcargs[arg]
       coro = testfunction(**testargs)  # Will not execute the test yet!

       # Run the coro in the event loop
       loop = testargs.get('loop', asyncio.get_event_loop())
       loop.run_until_complete(coro)

       return True


This is tested with pytest 2.6 and 2.7.  Maybe newer releases of pytest will
include something like this out-of-the-box.
