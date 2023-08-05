edeposit.amqp package
=====================

Purpose of this module is to provide class for launching Unix daemons
(:class:`daemonwrapper <edeposit.amqp.daemonwrapper>`), generict AMQP
communication service based on RabbitMQ's `pika
<http://pika.readthedocs.org/en/latest/>`_ library
(:class:`pikadaemon <edeposit.amqp.pikadaemon>`), specific AMQP communication
service for edeposit project (:class:`amqpdaemon <edeposit.amqp.amqpdaemon>`)
and also AMQP communication classes for sub-modules used in edeposit
project:

- :mod:`edeposit_amqp_alephdaemon` (AMQP wrapper for the
  `edeposit.amqp.aleph <http://edeposit-amqp-aleph.readthedocs.org>`_)
- :mod:`edeposit_amqp_calibredaemon` (AMQP wrapper for the
  `edeposit.amqp.calibre <http://edeposit-amqp-calibre.readthedocs.org>`_)
- :mod:`edeposit_amqp_ftp_managerd` (user management AMQP wrapper for the
  `edeposit.amqp.ftp <http://edeposit-amqp-ftp.readthedocs.org>`_)
- :mod:`edeposit_amqp_ftp_monitord` (AMQP binding for FTP event monitor -
  `edeposit.amqp.ftp <http://edeposit-amqp-ftp.readthedocs.org>`_)
- :mod:`edeposit_amqp_antivirusd` (AMQP wrapper for the ClamAV daemon
  `edeposit.amqp.antivirus <http://edeposit-amqp-antivirus.readthedocs.org>`_)
- :mod:`edeposit_amqp_harvester` (AMQP wrapper for the harvester module
  `edeposit.amqp.harvester <http://edeposit-amqp-harvester.readthedocs.org>`_)
- :mod:`edeposit_amqp_ltpd` (AMQP wrapper for the LTP export module
  `edeposit.amqp.ltp <http://edeposit-amqp-ltp.readthedocs.org>`_)
- :mod:`edeposit_amqp_pdfgend` (AMQP binding for PDF generator
  `edeposit.amqp.pdfgen <http://edeposit-amqp-pdfgen.readthedocs.org>`_)
- :mod:`edeposit_amqp_downloaderd` (AMQP binding for downloader
  `edeposit.amqp.downloader <http://edeposit-amqp-downloader.readthedocs.org>`_)
- :mod:`edeposit_amqp_storaged` (AMQP binding for storage subsystem
  `edeposit.amqp.storage <http://edeposit-amqp-storage.readthedocs.org>`_)

For example :mod:`edeposit_amqp_alephdaemon` script allows 
you to send simple requests to get data from Aleph (system used in libraries
all around the world) and in later versions also requests to put data into
Aleph.
Details of protocol and communication with Aleph server are handled by
`edeposit.amqp.aleph <https://github.com/edeposit/edeposit.amqp.aleph>`_ module.

Communication with sub-modules
------------------------------
From **user perspective**, communication is very similar to RPC - to each
`Request` is returned `Response`.

.. image:: /_static/communication.png

Note:
    `Requests` and `Responses` are identified and paired by `UUID`, which is
    transported in headers of AMQP message.

Request
+++++++
To send a request, you just need to send serialized structure (
:py:func:`collections.namedtuple`)
to the input queue of the daemon.

For example - for querying Aleph, take one of the Request classes, which
are defined in aleph's ``__init__.py``, into the RabbitMQ's exchange defined in
``settings.RABBITMQ_ALEPH_EXCHANGE``.

Serialization can be done by calling
:func:`~edeposit.amqp.serializers.serializers.serialize` function from
`edeposit.amqp.serializers`_.

.. _edeposit.amqp.serializers: http://edepositamqpserializers.readthedocs.org

Example showing how to send data to proper exchange::

    import uuid

    import settings
    from alephdaemon import getConnectionParameters
    from edeposit.amqp.serializers import serialize

    connection = pika.BlockingConnection(alephdaemon.getConnectionParameters())
    channel = connection.channel()

    UUID = uuid.uuid4()  # this will be used to pair request with response

    # put request together
    json_data = serialize(
        aleph.SearchRequest(
            aleph.ISBNQuery("80-251-0225-4")
        )
    )

    # create properties of message - notice particularly the UUID parameter
    properties = pika.BasicProperties(
        content_type="application/json",
        delivery_mode=1,
        headers={"UUID": str(UUID)}
    )

    # send the message to proper exchange with proper routing key
    channel.basic_publish(
        exchange=settings.RABBITMQ_ALEPH_EXCHANGE,
        routing_key=settings.RABBITMQ_ALEPH_INPUT_KEY,
        properties=properties,
        body=json_data
    )

It looks kinda long, but it is really simple and the most important thing in
respect to communication with module is::

    from edeposit.amqp.serializers import serialize

    json_data = serialize(
        aleph.SearchRequest(
            aleph.ISBNQuery("80-251-0225-4")
        )
    )

Here you say, that you want to perform `SearchRequest` and specifically search
for ISBN.

Another important thing is to send and save for later use the `UUID`. You want
to do this to be able to pair the response with request.

Warning:
    Messages received without `UUID` are thrown away without any warning.

Note:
    Notice also the `routing_key` parameter of ``channel.basic_publish()``. It
    is used to determine into which queue will be message delivered.


Response
++++++++
Response message is sent into ``settings.RABBITMQ_ALEPH_EXCHANGE`` with routing
key ``settings.RABBITMQ_ALEPH_OUTPUT_KEY``.

Format of response is usually one of the `*Response` classes from
``aleph.__init__.py`` serialized to JSON, so you may need to
:func:`~edeposit.amqp.serializers.serializers.deserialize` it. In headers,
there should always be the `UUID` parameter, even in case of some unexpected
error.

You can detect errors by looking for ``exception`` key in ``parameters.headers``
dictionary::

    for method_frame, properties, body in self.channel.consume(self.queue):
        headers = properties.headers
        if "exception" in headers:
            print "There was an error in processing request ", headers["UUID"]
            print headers["exception_name"] + ": " + headers["exception"]
            break

Details of exception are contained in ``exception``, ``exception_name`` and
``exception_type`` keys of the headers dictionary. First is text of error
message, second is the ``.__class__.__name__`` property of exception and third
is just output from ``type(exception)``.

Programmers perspective
-----------------------
If you want to add new module, you will have to create your own instance of
the :class:`.AMQPDaemon` and your module has to have some variant of the
:func:`.reactToAMQP` function. See :class:`.AMQPDaemon` doc-string for details.


Tips and tricks
---------------
Before you start sending the data, it is usually good idea to start the daemon.
RabbitMQ will hold the data even when the daemon is not running, but you won't
get the data back.

To start the daemon, run::

    edeposit_amqp_alephdaemon.py start

This will start the proper unix daemon listening for the requests at RabbitMQ's
message queue defined by :attr:`settings.RABBITMQ_ALEPH_INPUT_QUEUE
<edeposit.amqp.settings.RABBITMQ_ALEPH_INPUT_QUEUE>`.

Note:
    Message queues, exchanges and routing keys have to be defined in RabbitMQ
    before you start the daemon.

If you don't want to define all details of AMQP communication by yourself, you
can just run the :class:`edeposit_amqp_tool.py <edeposit_amqp_tool>`, which can
build the schema::

    edeposit_amqp_tool.py --host ftp --create

output example::

  Created exchange 'ftp'.
  Creating queues:
    Created durable queue 'daemon'.
    Created durable queue 'plone'.

  Routing exchanges using routing key to queues:
    Routing exchange ftp['request'] -> 'daemon'.
    Routing exchange ftp['result'] -> 'plone'.

Project structure
-----------------
Here is pseudo-UML picture documenting relations between module components.

.. image:: /_static/structure.png
    :width: 800px

List of submodules
++++++++++++++++++

.. toctree::
   :maxdepth: 1

   /api/edeposit.amqp.daemonwrapper.rst
   /api/edeposit.amqp.pikadaemon.rst
   /api/edeposit.amqp.amqpdaemon.rst
   /api/edeposit.amqp.settings.rst

List of scripts
+++++++++++++++
Following scrips are installed to user's ``/bin`` directory and therefore
can be called by simply typing their name to the shell:

.. toctree::
   :maxdepth: 1

   /api/edeposit.amqp.alephdaemon.rst
   /api/edeposit.amqp.calibredaemon.rst
   /api/ftp_managerd.rst
   /api/ftp_monitord.rst
   /api/edeposit.amqp.antivirus.rst
   /api/harvester.rst
   /api/ltpd.rst
   /api/pdfgend.rst
   /api/downloaderd.rst
   /api/storaged.rst

.. toctree::
   :maxdepth: 1

   /api/edeposit.amqp.tool.rst
