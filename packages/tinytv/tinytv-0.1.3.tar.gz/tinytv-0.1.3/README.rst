===============================
ShowRss.info ncurses interface
===============================

.. image:: https://img.shields.io/pypi/v/tinytv.svg
        :target: https://pypi.python.org/pypi/tinytv


Ncurses interface for downloading showrss.info series, and keeping track of the watched / not watched episodes

* Free software: BSD license
* Documentation: https://tinytv.readthedocs.org.

Features
--------

* NCurses interface for showrss.info using libtorrent streaming
* NCurses interface for IMDB + KAT using libtorrent streaming
* NCurses interface for direct magnet links lists (just magnets, one at a line)


Usage
-----

::

    usage: tinytv [-h] [--showrss_url [SHOWRSS_URL]] {imdb,showrss,magnet}

    tinytv

    positional arguments:
      {imdb,showrss,magnet}
                            Interface

    optional arguments:
      -h, --help            show this help message and exit
      --showrss_url [SHOWRSS_URL]
                            Showrss rss url


ShowRSS
++++++++

This uses a showrss.info RSS feed to build an interface and stream.

.. image:: /docs/nshowrss.png?raw=true
.. image:: /docs/chapters.png?raw=true

Magnet
++++++

Given a list of magnets, it'll try to discover its series title/season/chapter and
build an interface for it, with streaming support too.

IMDB
++++

Gets the most popular IMDB shows and builds an interface with them.
Tries to look the episodes on KAT (looks magnet links) once selected and streams it.

.. image:: /docs/imdb.png?raw=true
