Sailabove client

Sailabove.com is a docker hosting solution aiming to be as flexible as a
container and as elegant as a sailboat.

Setup
=====

.. code:: bash

    # get the CLI
    pip install sail

    # activate autocompletion support
    activate-global-python-argcomplete

Configuration
=============

``sail`` automatically loads registry's credentials from ``docker`` keyring.
Hence, after a succesfull push to Sailabove's registry, there should be no
need for configuration.

If you wish to temporarily override a parameter, you may use ``SAIL_HOST``,
``SAIL_USER`` and ``SAIL_PASSWORD`` to respectively force the API endpoint,
the username and the password. Additionally, these parameters may be set via
``--api-host``, ``--api-user`` and ``--api-password``

Usage
=====

Once you have claimed your private namespace on http://labs.runabove.com/docker and
sucessfuly pushed your first image you may launch and supervice a service
from this template image. For example, taking a ``my-redis`` Docker, let's
create a ``redis`` service:

.. code:: bash

    sail services add my-redis redis

Watch your private cluster's status:

.. code:: bash

    sail services ps

Scale your cluster:

.. code:: bash

    sail services scale redis --number 2

Clear everything:

.. code:: bash

    sail services rm redis

Troubleshooting
===============

urllib3 SSL warning
-------------------

If you get spurious warnings regarding SSL like:

.. code:: bash

    /usr/local/lib/python2.7/dist-packages/requests/packages/urllib3/util/ssl_.py:90: InsecurePlatformWarning: A true SSLContext object is not available. This prevents urllib3 from configuring SSL appropriately and may cause certain SSL connections to fail. For more information, see https://urllib3.readthedocs.org/en/latest/security.html#insecureplatformwarning.
  InsecurePlatformWarning
    /usr/local/lib/python2.7/dist-packages/requests/packages/urllib3/util/ssl_.py:90: InsecurePlatformWarning: A true SSLContext object is not available. This prevents urllib3 from configuring SSL appropriately and may cause certain SSL connections to fail. For more information, see https://urllib3.readthedocs.org/en/latest/security.html#insecureplatformwarning.
  InsecurePlatformWarning

You may fix it by manually installing the package ``requests[security]``. This package requires ``gcc`` to build, this is the reason why we do not include it by defaul.

.. code:: bash

    sudo apt-get install python-dev libffi-dev build-essential
    sudo pip install requests[security]

Related links
=============

- **Sign Up**: http://labs.runabove.com/docker
- **Registry**: https://registry.sailabove.io/
- **Get help**: https://community.runabove.com/
- **Get started**: https://community.runabove.com/kb/en/docker/getting-started-with-sailabove-docker.html
- **Documentation**: `Reference documentation<https://community.runabove.com/kb/en/docker/documentation>`_, `Guides<http://community.runabove.com/kb/en/docker/>`_
- **OVH Docker mailing-list**: docker-subscribe@ml.ovh.net

