docker-wrapper-py |Build status| |Coverage status|
==================================================

Install
-------

::

    pip install docker-wrapper

Usage
-----

Use it in a with statement:

.. code:: python

    with Docker() as docker:
        docker.run('command')

or as a decorator:

.. code:: python

        @Docker.wrap()
        def run_command_in_container(command, docker)
            docker.run(command)

Read the documentation on
`docker-wrapper-py.readthedocs.org <http://docker-wrapper-py.readthedocs.org>`__
for more information about how to use this.

--------------

MIT © frigg.io

.. |Build status| image:: https://ci.frigg.io/badges/frigg/docker-wrapper-py/
   :target: https://ci.frigg.io/frigg/docker-wrapper-py/last/
.. |Coverage status| image:: https://ci.frigg.io/badges/coverage/frigg/docker-wrapper-py/
   :target: https://ci.frigg.io/frigg/docker-wrapper-py/last/


