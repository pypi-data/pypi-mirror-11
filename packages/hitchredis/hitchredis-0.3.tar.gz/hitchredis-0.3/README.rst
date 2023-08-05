HitchRedis
==========

HitchRedis is a plugin for the Hitch testing framework that lets you run and
interact with Redis during your integration tests.


Use with Hitch
==============

Install like so::

    $ hitch install hitchredis


.. code-block:: python

        # Service definition in engine's setUp:
        self.services['Redis'] = hitchredis.RedisService(
            version="2.8.4"                                     # Mandatory
            redis_exec="redis-server",                          # Optional (default: redis-server)
            redis_cli="redis-cli",                              # Optional (default: redis-cli)
            port=16379,                                         # Optional (default: 16379)
        )

        # Interact using the cli:
        self.services['Redis'].cli("-n", "1", "get", "mypasswd").run()
        [ prints mypasswd ]


See this service in action at the DjangoRemindMe_ project.


Features
========

* Starts up on a separate thread in parallel with other services when running with HitchServe_, so that your integration tests run faster.
* Contains subcommand to interact with the CLI.
* Run the server on whichever port you like.
* Version must be set explicitly to prevent "works on my machine" screw ups caused by different versions of Redis being installed.


.. _HitchServe: https://github.com/hitchtest/hitchserve
.. _DjangoRemindMe: https://github.com/hitchtest/django-remindme
