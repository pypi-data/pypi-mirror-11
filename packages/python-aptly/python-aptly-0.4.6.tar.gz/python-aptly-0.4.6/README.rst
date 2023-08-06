============
python-aptly
============

Aptly REST API client and useful tooling

.. attention:: This application is in early development stage. Every help or feedback is appreciated.

Publisher
=========

Publisher is tool for publishing latest snapshots.
It takes configuration in yaml format which defines what to publish and how.

Publisher expects snapshots in format ``<name>-<timestamp>``.

Features
--------

- create or update publish from latest snapshots
- promote publish

  - use it's snapshots to create or update another publish (eg. testing ->
    stable)

- cleanup unused snapshots

Create or update publish
~~~~~~~~~~~~~~~~~~~~~~~~

First create configuration file where you define Aptly repositories, mirrors
and target distributions for publishing.

.. code-block:: yaml

    mirror:
      # Ubuntu upstream repository
      trusty-main:
        # Base for our main component
        component: main
        distributions:
          - nightly/trusty
      # Mirrored 3rd party repository
      aptly:
        # Merge into main component
        component: main
        distributions:
          - nightly/trusty

    repo:
      # Some repository with custom software
      cloudlab:
        # Publish as component cloudlab
        component: cloudlab
        distributions:
          # We want to publish our packages (that can't break anything for
          sure) immediately to both nightly and testing
          # repositories
          - nightly/trusty
          - testing/trusty

Configuration above will create two publishes from latest snapshots of
defined repositories and mirrors:

1. ``nightly/trusty`` with component cloudlab and main (created snapshot
  main-`<timestamp>` by merging snapshots aptly-`<timestamp>` and
  trusty-main-`<timestamp>` snapshots)
2. ``testing/trusty`` with component cloudlab, made of repository cloudlab

It expects that snapshots are already created (by mirror syncing script or by
CI when new package is built) so it does following:

- find latest snapshot (by creation date) for each defined mirror and
  repository

  - snapshots are recognized by name (eg. ``cloudlab-<timestamp>``,
  ``trusty-main-<timestamp>``)

- create new snapshot by merging snapshots with same component (eg. create
  ``_main-<timestamp>`` from latest ``trusty-main-<timestamp>`` and
  ``aptly-<timestamp>`` snapshots

  - merged snapshots are prefixed by ``_`` to avoid collisions with other
    snapshots
  - first it checks if merged snapshots already exists and if so, it will skip
    creation of duplicated snapshot. So it's tries to be fully idempotent.

- create or update publish or publishes as defined in configuration

It can be executed like this:

::

  aptly-publisher -c config.yaml -v --url http://localhost:8080 publish

Promote publish
~~~~~~~~~~~~~~~

Let's assume you have following prefixes and workflow:

- nightly

  - created by `publish` action when there's new snapshot or synced mirror
  - packages are always up to date

- testing

  - freezed repository for testing and stabilization

- stable

  - well tested package versions
  - well controlled update process

There can be more publishes under prefix, eg. ``nightly/trusty``,
``nightly/vivid``

Then you need to switch published snapshots from one publish to another one.

::

  aptly-publisher -v --url http://localhost:8080  \
  --source nightly/trusty --target testing/trusty \
  publish

You can also specify list of components. When you have separate components for
your packages (eg. cloudlab) and security (mirror of trusty security
repository), you may need to release them faster.

::

  aptly-publisher -v --url http://localhost:8080  \
  --source nightly/trusty --target testing/trusty \
  --components cloudlab security -- publish

Cleanup unused snapshots
~~~~~~~~~~~~~~~~~~~~~~~~

When you are creating snapshots regularly, you need to delete old ones that
are not used by any publish. It's wise to call such action every time when
publish is updated (eg. nightly).

::

  aptly-publisher -v --url http://localhost:8080 cleanup

TODO
----

There are still things left to do.

- action to show differences between publishes

  - to see which snapshots are going to be promoted
  - ..and which packages with them
  - it would be also nice to be able to see changelog of such packages

Build
=====

You can install directly using ``python setup.py install`` or better build
Debian package with eg.:

::

  dpkg-buildpackage -uc -us

Read more
=========

For usage informations, see ``aptly-publisher --help`` or man page.

::

  man man/aptly-publisher.1

Known issues
============

- determine source snapshots correctly
  (`#271 <https://github.com/smira/aptly/issues/271>`_)
- cleanup merged snapshots before cleaning up source ones

  - before that it's needed to run cleanup action multiple times to get all
    unused snapshots cleaned
