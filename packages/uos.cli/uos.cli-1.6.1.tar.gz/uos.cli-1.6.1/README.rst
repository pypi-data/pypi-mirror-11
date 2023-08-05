=======
UOS CLI
=======

UOS CLI is forked from OpenStackClient, and is designed for `UOS`_
operations which use commmand 'uos' instead of 'openstack'.

.. _UOS: https://www.ustack.com

OpenStackClient
===============

OpenStackClient (aka OSC) is a command-line client for OpenStack that brings
the command set for Compute, Identity, Image, Object Store and Volume APIs
together in a single shell with a uniform command structure.

The primary goal is to provide a unified shell command structure and a common
language to describe operations in OpenStack.

* `PyPi`_ - package installation
* `Online Documentation`_
* `Launchpad project`_ - release management
* `Blueprints`_ - feature specifications
* `Bugs`_ - issue tracking
* `Source`_
* `Developer` - getting started as a developer
* `Contributing` - contributing code
* IRC: #openstack-sdks on Freenode (irc.freenode.net)
* License: Apache 2.0

.. _PyPi: https://pypi.python.org/pypi/python-openstackclient
.. _Online Documentation: http://docs.openstack.org/developer/python-openstackclient/
.. _Launchpad project: https://launchpad.net/python-openstackclient
.. _Blueprints: https://blueprints.launchpad.net/python-openstackclient
.. _Bugs: https://bugs.launchpad.net/python-openstackclient
.. _Source: https://git.openstack.org/cgit/openstack/python-openstackclient
.. _Developer: http://docs.openstack.org/infra/manual/python.html
.. _Contributing: http://docs.openstack.org/infra/manual/developers.html

Getting Started
===============

UOS CLI can be installed from PyPI using pip::

    pip install uos.cli

There are a few variants on getting help.  A list of global options and supported
commands is shown with ``--help``::

    uos --help

There is also a ``help`` command that can be used to get help text for a specific
command::

    uos help
    uos help server create

Configuration
=============

Get uosrc from `console`_, edit uosrc and set your password.

.. _console: https://console.ustack.com

Example
=======

::

    % source uosrc
    % uos
    (uos) help

    Shell commands (type help <topic>):
    ===================================
    cmdenvironment  edit  hi       l   list  pause  r    save  shell      show
    ed              help  history  li  load  py     run  set   shortcuts

    Undocumented commands:
    ======================
    EOF  eof  exit  q  quit

    Application commands (type help <topic>):
    =========================================
    access token create         ip fixed add                  service provider list
    aggregate add host          ip fixed remove               service provider set
    aggregate create            ip floating add               service provider show
    aggregate delete            ip floating create            service set
    aggregate list              ip floating delete            service show
    aggregate remove host       ip floating list              snapshot create
    aggregate set               ip floating pool list         snapshot delete
    aggregate show              ip floating remove            snapshot list
    availability zone list      keypair create                snapshot set
    backup create               keypair delete                snapshot show
    backup delete               keypair list                  snapshot unset
    backup list                 keypair show                  token issue
    backup restore              limits show                   trust create
    backup show                 mapping create                trust delete
    catalog list                mapping delete                trust list
    catalog show                mapping list                  trust show
    command list                mapping set                   usage list
    complete                    mapping show                  usage show
    compute agent create        module list                   user create
    compute agent delete        network create                user delete
    compute agent list          network delete                user list
    compute agent set           network list                  user password set
    compute service list        network set                   user set
    compute service set         network show                  user show
    console log show            policy create                 volume create
    console url show            policy delete                 volume delete
    consumer create             policy list                   volume list
    consumer delete             policy set                    volume set
    consumer list               policy show                   volume show
    consumer set                project create                volume type create
    consumer show               project delete                volume type delete
    credential create           project list                  volume type list
    credential delete           project set                   volume type set
    credential list             project show                  volume type unset
    credential set              project usage list            volume unset
    credential show             quota set
    domain create               quota show
    domain delete               region create
    domain list                 region delete
    domain set                  region list
    domain show                 region set
    ec2 credentials create      region show
    ec2 credentials delete      request token authorize
    ec2 credentials list        request token create
    ec2 credentials show        role add
    endpoint create             role assignment list
    endpoint delete             role create
    endpoint list               role delete
    endpoint set                role list
    endpoint show               role remove
    extension list              role set
    federation domain list      role show
    federation project list     security group create
    federation protocol create  security group delete
    federation protocol delete  security group list
    federation protocol list    security group rule create
    federation protocol set     security group rule delete
    federation protocol show    security group rule list
    flavor create               security group set
    flavor delete               security group show
    flavor list                 server add security group
    flavor set                  server add volume
    flavor show                 server create
    flavor unset                server delete
    group add user              server image create
    group contains user         server list
    group create                server lock
    group delete                server migrate
    group list                  server pause
    group remove user           server reboot
    group set                   server rebuild
    group show                  server remove security group
    help                        server remove volume
    host list                   server rescue
    host show                   server resize
    hypervisor list             server resume
    hypervisor show             server set
    hypervisor stats show       server show
    identity provider create    server ssh
    identity provider delete    server suspend
    identity provider list      server unlock
    identity provider set       server unpause
    identity provider show      server unrescue
    image create                server unset
    image delete                service create
    image list                  service delete
    image save                  service list
    image set                   service provider create
    image show                  service provider delete