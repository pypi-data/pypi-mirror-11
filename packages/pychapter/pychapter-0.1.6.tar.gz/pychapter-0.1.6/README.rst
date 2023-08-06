===============================
pychapter
===============================

.. image:: https://img.shields.io/travis/Xayon/pychapter.svg
        :target: https://travis-ci.org/Xayon/pychapter

.. image:: https://img.shields.io/pypi/v/pychapter.svg
        :target: https://pypi.python.org/pypi/pychapter


Chapter management tool with support for magnet links and filenames

* Free software: BSD license
* Documentation: https://pychapter.readthedocs.org.

Features
--------

* TODO
* Given a magnet link, return TV a Chapter object with tv chapter data (filename, series, season, chapter)

Usage
-----


This is a simple library, to use it just:

::

    >>> Chapter(magnet='magnet:?xt=urn:btih:57aebdc26ceebf6f3c0ae69666fdd7fcfe09a1fd&dn=Ghost.Adventures.S11E02.Old.Montana.State.Prison.720p.HDTV.x264-DHD%5Brartv%5D&tr=http%3A%2F%2Ftracker.trackerfix.com%3A80%2Fannounce&tr=udp%3A%2F%2F9.rarbg.me%3A2710&tr=udp%3A%2F%2F9.rarbg.to%3A2710')

    Chapter 11x2 - Old Montana State Prison

This returns the Chapter object representation for a given magnet link, wich is "Chapter {Season}x{episode} - {SeriesName}"

You can also play it using http://github.com/XayOn/python-SimpleTorrentStreaming/ with "play" method:

::


    >> Chapter(magnet='magnet:?xt=urn:btih:57aebdc26ceebf6f3c0ae69666fdd7fcfe09a1fd&dn=Ghost.Adventures.S11E02.Old.Montana.State.Prison.720p.HDTV.x264-DHD%5Brartv%5D&tr=http%3A%2F%2Ftracker.trackerfix.com%3A80%2Fannounce&tr=udp%3A%2F%2F9.rarbg.me%3A2710&tr=udp%3A%2F%2F9.rarbg.to%3A2710').play()

This will launch the episode with mplayer
