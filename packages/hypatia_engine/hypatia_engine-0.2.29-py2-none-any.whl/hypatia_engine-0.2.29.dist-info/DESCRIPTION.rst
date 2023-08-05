Hypatia 0.2.29 (alpha)
======================

.. figure:: https://lillian-lemmer.github.io/hypatia/media/logos/logotype-blacktext-transparentbg.png
   :alt: Hypatia 0.2

   Hypatia 0.2

|GitHub license| |PyPI Version| |Travis| |Coveralls| |Code Climate|
|PyPI Popularity| |Gratipay| |Bountysource| |Donate with Paypal| |Donate
with Patreon| |My Amazon Wishlist|

Make 2D action adventure games. For programmers and nonprogrammers
alike.

Create a games like `*Legend of Zelda: Oracle of Ages* and *Oracle of
Seasons* <http://en.wikipedia.org/wiki/The_Legend_of_Zelda:_Oracle_of_Seasons_and_Oracle_of_Ages>`__.

The included demo game (``demo/game.py``) in action:

.. figure:: http://lillian-lemmer.github.io/hypatia/media/recordings/2015-06-28-develop-640x480.gif
   :alt: The demo game in action.

   The demo game in action.

`Cross-platform (Windows, Mac, Linux, BSD), putting FreeBSD development
first. <https://github.com/lillian-lemmer/hypatia/wiki/Platform-Support>`__

A labor of love, `permissively (MIT)
licensed <https://raw.githubusercontent.com/lillian-lemmer/hypatia/master/LICENSE>`__,
and crafted by `Lillian
Lemmer <http://github.com/lillian-lemmer/hypatia/wiki/About-the-Creator>`__.

`Please read about how you can help support
Hypatia! <https://github.com/lillian-lemmer/hypatia/wiki/Support-the-Project>`__

Resources
=========

-  `Installation
   instructions <https://github.com/lillian-lemmer/hypatia/wiki/Installation-Instructions>`__.
-  `Hypatia Wiki <https://github.com/lillian-lemmer/hypatia/wiki/>`__
   (great resource for nonprogrammers, too!)
-  `Hypatia API Docs <https://lillian-lemmer.github.io/hypatia/api>`__
-  For people, checkout the `socialization and contact methods for the
   Hypatia
   project <https://github.com/lillian-lemmer/hypatia/wiki/Profiles>`__.
-  `The official Hypatia
   website <http://lillian-lemmer.github.io/hypatia/>`__
-  Official support chat: `#hypatia on Freenode
   (webui!) <http://webchat.freenode.net/?channels=hypatia>`__
-  You can contact the author via email: lillian.lynn.lemmer@gmail.com,
   [@LilyLemmer](https:/twitter.com/LilyLemmer) on Twitter.

To know your way around the project, I strongly recommend reading the
`CONTRIBUTING.md <https://github.com/lillian-lemmer/hypatia/blob/master/CONTRIBUTING.md>`__
file. It covers everything you need to know about contributing to
Hypatia, as well as navigating the project.

Dive in without any programming
===============================

The included demo allows you to mess with all of its resources (see the
``resources`` directory!). With it you can:

-  `Create tilesheets to make
   tilemaps <https://github.com/lillian-lemmer/hypatia/wiki/Tilesheets>`__

   -  Configure tiles from the tilesheet
   -  Chain tiles together to create animations
   -  Apply the "cycle" effect, which takes a non-animated tile, and
      creates an animated tile by rotating the colors used in the tile
   -  Set tile flags, like the ``impass_all`` flag which makes a flag
      impassable to the player

-  `Create tilemaps with an arbitrary number of layers, using plaintext
   files <https://github.com/lillian-lemmer/hypatia/wiki/tilemap.txt>`__
-  `Create scenes, with configurable NPCs, configurable scene data
   (player start
   position) <https://github.com/lillian-lemmer/hypatia/wiki/Nonprogrammer-Guide#editing-scene-data>`__

   -  You can create scenes from a Tiled editor TMX file.

-  `Create character sprites using animated or non-animated
   GIFs <https://github.com/lillian-lemmer/hypatia/wiki/Walkabout-Sprites>`__

For more information, please read the `official wiki guide for
non-programmers <https://github.com/lillian-lemmer/hypatia/wiki/Nonprogrammer-Guide>`__.

Quick Demo
==========

Windows
-------

Simply run ``game.exe`` after extracting
`hypatia-demo-windows-current.zip <https://lillian-lemmer.github.io/hypatia/releases/hypatia-demo-windows-current.zip>`__.

Other
-----

To get setup quickly and start tinkering around with the demo, simply
issue the following commands:

1. ``pip install hypatia_engine``
2. ``cd demo``
3. ``python game.py``

.. |GitHub license| image:: https://img.shields.io/github/license/lillian-lemmer/hypatia.svg?style=flat-square
   :target: https://raw.githubusercontent.com/lillian-lemmer/hypatia/master/LICENSE
.. |PyPI Version| image:: https://img.shields.io/pypi/v/hypatia_engine.svg?style=flat-square
   :target: https://pypi.python.org/pypi/hypatia_engine/
.. |Travis| image:: https://img.shields.io/travis/lillian-lemmer/hypatia.svg?style=flat-square
   :target: https://travis-ci.org/lillian-lemmer/hypatia
.. |Coveralls| image:: https://img.shields.io/coveralls/lillian-lemmer/hypatia.svg?style=flat-square
   :target: https://coveralls.io/r/lillian-lemmer/hypatia
.. |Code Climate| image:: https://img.shields.io/codeclimate/github/lillian-lemmer/hypatia.svg?style=flat-square
   :target: https://codeclimate.com/github/lillian-lemmer/hypatia
.. |PyPI Popularity| image:: https://img.shields.io/pypi/dm/hypatia_engine.svg?style=flat-square
   :target: https://pypi.python.org/pypi/hypatia_engine/
.. |Gratipay| image:: https://img.shields.io/gratipay/lillian-lemmer.svg?style=flat-square
   :target: https://gratipay.com/~lillian-lemmer/
.. |Bountysource| image:: https://img.shields.io/bountysource/team/hypatia/activity.svg?style=flat-square
   :target: https://www.bountysource.com/teams/hypatia
.. |Donate with Paypal| image:: https://img.shields.io/badge/paypal-donate-ff69b4.svg?style=flat-square
   :target: https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=YFHB5TMMXMNT6
.. |Donate with Patreon| image:: https://img.shields.io/badge/patreon-donate%20monthly-ff69b4.svg?style=flat-square
   :target: https://www.patreon.com/lilylemmer
.. |My Amazon Wishlist| image:: https://img.shields.io/badge/amazon%20wishlist-buy%20me%20things-ff69b4.svg?style=flat-square
   :target: http://amzn.com/w/NKBZ0CX162S9


