===============
with-aws-config
===============

Set AWS `environment variables`_ from the configuration files maintained by
`aws configure`_, then run a command.

.. _aws configure: http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html

-----
Usage
-----

``with-aws-config [-h] [--verbose] [--profile PROFILE] COMMAND [ARGUMENT ...]``

~~~~~~~~~~~~~~~~~~~~
Positional arguments
~~~~~~~~~~~~~~~~~~~~

``COMMAND``
  the command to run, e.g. ``ec2-describe-instances``, ``aws``, or ``ansible``
``ARGUMENT``
  the command's arguments, e.g. ``iam get-user``

If any arguments are options, specify ``--`` before the command to end
``with-aws-config``'s optional argument parsing.

~~~~~~~~~~~~~~~~~~
Optional arguments
~~~~~~~~~~~~~~~~~~

``-h, --help``
  show this help message and exit
``--verbose``, ``-v``
  output debugging information to stderr
``--profile PROFILE``, ``-p PROFILE``
  set the profile, ignoring any `environment variables`_

---------
Behaviour
---------

``with-aws-config``:

* Loads profile information stored by ``aws configure``
* Runs the `command and arguments`_ with `adjusted environment variables`_, and
* Exits with its `exit status`_ if possible.

You have three ways to specify the profile:

* Default to ``default``
* Give the ``--profile`` or ``-p`` `optional arguments`_
* Set the ``AWS_PROFILE`` or ``AWS_DEFAULT_PROFILE`` `input environment variables`_

.. _option: `optional arguments`_
.. _adjusted environment variables: output_
.. _input environment variables: input_
.. _command and arguments: `positional arguments`_
.. _aws cli: https://aws.amazon.com/documentation/cli/
.. _ec2 cli: https://aws.amazon.com/developertools/351
.. _ansible: http://www.ansible.com/home
.. _boto: http://docs.pythonboto.org/en/latest/

--------
Examples
--------

Run a command:

  ::

    with-aws-config -- aws iam get-user
    with-aws-config -- ec2-list-instances
    with-aws-config -- ansible-playbook setup-vpc.yaml

Specify a profile as an option:

  ::

    with-aws-config --profile=default -- ec2-describe-instances

Specify a profile via the environment:

  ::

    env AWS_DEFAULT_PROFILE=default with-aws-config -- ec2-describe-instances

Note we've used ``--`` in each to force the end of the `optional arguments`_.

---------------------
Environment Variables
---------------------

~~~~~
Input
~~~~~

* ``AWS_PROFILE`` is used to specify profile if ``--profile`` is not given
* ``AWS_DEFAULT_PROFILE`` is used if ``AWS_PROFILE`` is not set
* ``HOME`` is required to locate ``$HOME/.aws``

~~~~~~
Output
~~~~~~

``COMMAND`` will be run with the environment supplied to ``with-aws-config``,
with the following exceptions:

The following environment variables will be removed:

* ``AWS_CONFIG_FILE``
* ``AWS_DEFAULT_PROFILE``
* ``AWS_PROFILE``
* ``AWS_SESSION_TOKEN``

The following environment variables will be set based on the AWS profile:

* ``AWS_ACCESS_KEY``
* ``AWS_ACCESS_KEY_ID``
* ``AWS_DEFAULT_REGION``
* ``AWS_SECRET_ACCESS_KEY``
* ``AWS_SECRET_KEY``
* ``EC2_URL``

``AWS_DEFAULT_REGION`` and ``EC2_URL`` will default to point to ``us-west-2``
if not configured during ``aws configure``.

Why this many?

* ``aws``, ``boto``, and ``ansible`` need ``AWS_ACCESS_KEY_ID``,
  ``AWS_SECRET_ACCESS_KEY``, and ``AWS_DEFAULT_REGION``

* ``ec2-*`` need ``AWS_ACCESS_KEY``, ``AWS_SECRET_KEY``, and ``EC2_URL``

-----------
Exit Status
-----------

``with-aws-config`` exits with either:

* The exit status of ``COMMAND`` or, if it can't be run:
* One of the following status codes indicating why:

  :``124``: no configuration files found
  :``125``: no configuration section found for the requested profile
  :``127``: command not found
  :``130``: interrupted by user with ^C
