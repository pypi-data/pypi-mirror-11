You-Get
=======

|Build Status| |PyPI version| |Gitter|

`You-Get <http://www.soimort.org/you-get>`__ is a video downloader for
`YouTube <http://www.youtube.com>`__, `Youku <http://www.youku.com>`__,
`niconico <http://www.nicovideo.jp>`__ and a few other sites.

``you-get`` is a command-line program, written completely in Python 3.
Its prospective users are those who prefer CLI over GUI. With
``you-get``, downloading a video is just one command away:

::

    $ you-get http://youtu.be/sGwy8DsUJ4M

Fork me on GitHub: https://github.com/soimort/you-get

Features
--------

Supported Sites
~~~~~~~~~~~~~~~

-  Dailymotion http://dailymotion.com
-  Freesound http://www.freesound.org
-  Google+ http://plus.google.com
-  Instagram http://instagram.com
-  JPopsuki http://jpopsuki.tv
-  Magisto http://www.magisto.com
-  Mixcloud http://www.mixcloud.com
-  Niconico (ニコニコ動画) http://www.nicovideo.jp
-  Vimeo http://vimeo.com
-  Vine http://vine.co
-  Twitter http://twitter.com
-  Youku (优酷) http://www.youku.com
-  YouTube http://www.youtube.com
-  755 (ナナゴーゴー) http://7gogo.jp
-  AcFun http://www.acfun.tv
-  Alive.in.th http://alive.in.th
-  Baidu Music (百度音乐) http://music.baidu.com
-  Baidu Wangpan (百度网盘) http://pan.baidu.com
-  Baomihua (爆米花) http://video.baomihua.com
-  bilibili http://www.bilibili.com
-  Blip http://blip.tv
-  Catfun (喵星球) http://www.catfun.tv
-  CBS http://www.cbs.com
-  CNTV (中国网络电视台) http://www.cntv.cn
-  Coursera https://www.coursera.org
-  Dongting (天天动听) http://www.dongting.com
-  Douban (豆瓣) http://douban.com
-  DouyuTV (斗鱼) http://www.douyutv.com
-  eHow http://www.ehow.com
-  Facebook http://facebook.com
-  Fun.tv (风行, Funshion) http://www.fun.tv
-  Google Drive http://docs.google.com
-  ifeng (凤凰视频) http://v.ifeng.com
-  iQIYI (爱奇艺) http://www.iqiyi.com
-  iQilu (齐鲁网, 山东网络台) http://v.iqilu.com
-  Joy.cn (激动网) http://www.joy.cn
-  Khan Academy http://www.khanacademy.org
-  Ku6 (酷6网) http://www.ku6.com
-  Kugou (酷狗音乐) http://www.kugou.com
-  Kuwo (酷我音乐) http://www.kuwo.cn
-  LeTV (乐视网) http://www.letv.com
-  Lizhi.fm (荔枝FM) http://www.lizhi.fm
-  Metacafe http://www.metacafe.com
-  MioMio http://www.miomio.tv
-  MTV 81 http://www.mtv81.com
-  NetEase (网易视频) http://v.163.com
-  NetEase Music (网易云音乐) http://music.163.com
-  PPTV http://www.pptv.com
-  QianMo (阡陌视频) http://qianmo.com
-  QQ (腾讯视频) http://v.qq.com
-  Sina (新浪视频) http://video.sina.com.cn
-  Weibo Miaopai (新浪微博秒拍视频) http://video.weibo.com
-  Sohu (搜狐视频) http://tv.sohu.com
-  SongTaste http://www.songtaste.com
-  SoundCloud http://soundcloud.com
-  TED http://www.ted.com
-  Tudou (土豆) http://www.tudou.com
-  Tumblr http://www.tumblr.com
-  VID48 http://vid48.com
-  VideoBam http://videobam.com
-  VK http://vk.com
-  56 (56网) http://www.56.com
-  Xiami (虾米) http://www.xiami.com
-  YinYueTai (音悦台) http://www.yinyuetai.com
-  Zhanqi (战旗TV) http://www.zhanqi.tv/lives

Prerequisites
-------------

Python 3
~~~~~~~~

``you-get`` is known to work with:

-  Python 3.2
-  Python 3.3
-  Python 3.4
-  Python 3.5
-  PyPy3

Dependencies (Optional but Recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  `FFmpeg <http://ffmpeg.org>`__ or `Libav <http://libav.org/>`__

   -  For video and audio processing.

-  `RTMPDump <http://rtmpdump.mplayerhq.hu/>`__

   -  For RTMP stream processing.

Installation
------------

You don't have to learn the Python programming language to use this
tool. However, you need to make sure that Python 3 (with pip) is
installed on your system.

On Linux and BSD, installation made easy with your package manager:

-  Find and install packages: ``python3`` and ``python3-pip`` (if your
   distro did not make Python 3 the default, e.g., Debian)
-  Or packages: ``python`` and ``python-pip`` (if your distro made
   Python 3 the default, e.g., Arch)

On other systems (which tend to have quite evil user experience), please
read the documentation and ask Google for help:

-  https://www.python.org/downloads/
-  https://pip.pypa.io/en/latest/installing.html

1. Using Pip (Standard Method)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    $ [sudo] pip3 install you-get

Check if the installation is successful:

::

    $ you-get -V

2. Downloading from PyPI
~~~~~~~~~~~~~~~~~~~~~~~~

You can also download the Python wheel for each release from
`PyPI <https://pypi.python.org/pypi/you-get>`__.

If you choose to download the wheel from a PyPI mirror or elsewhere,
remember to verify the signature of the package. For example:

::

    $ gpg --verify you_get-0.3.30-py3-none-any.whl.asc you_get-0.3.30-py3-none-any.whl

3. Downloading from GitHub
~~~~~~~~~~~~~~~~~~~~~~~~~~

Download it `here <https://github.com/soimort/you-get/zipball/master>`__
or:

::

    $ wget -O you-get.zip https://github.com/soimort/you-get/zipball/master
    $ unzip you-get.zip

Use the raw script without installation:

::

    $ cd soimort-you-get-*/
    $ ./you-get -V

To install the package into the system path, execute:

::

    $ [sudo] make install

Check if the installation is successful:

::

    $ you-get -V

4. Using Git (Recommended for Developers and Advanced Users)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    $ git clone git://github.com/soimort/you-get.git

Use the raw script without installation:

::

    $ cd you-get/
    $ ./you-get -V

To install the package into the system path, execute:

::

    $ [sudo] make install

Check if the installation is successful:

::

    $ you-get -V

Upgrading
---------

1. Using Pip
~~~~~~~~~~~~

::

    $ [sudo] pip3 install --upgrade you-get

Getting Started
---------------

Display the information of a video without downloading:

::

    $ you-get -i 'http://www.youtube.com/watch?v=sGwy8DsUJ4M'

Download a video:

::

    $ you-get 'http://www.youtube.com/watch?v=sGwy8DsUJ4M'

Download multiple videos:

::

    $ you-get 'http://www.youtube.com/watch?v=sGwy8DsUJ4M' 'http://www.youtube.com/watch?v=8bQlxQJEzLk'

By default, program will skip any video that already exists in the local
directory when downloading. If a temporary file (ends with a
``.download`` extension in its file name) is found, program will resume
the download from last session.

To enforce re-downloading of videos, use option ``-f``: (this will
overwrite any existing video or temporary file)

::

    $ you-get -f 'http://www.youtube.com/watch?v=sGwy8DsUJ4M'

Set the output directory for downloaded files:

::

    $ you-get -o ~/Downloads 'http://www.youtube.com/watch?v=sGwy8DsUJ4M'

Use a specific HTTP proxy for downloading:

::

    $ you-get -x 127.0.0.1:8087 'http://www.youtube.com/watch?v=sGwy8DsUJ4M'

By default, the system proxy setting (i.e. environment variable
``http_proxy`` on \*nix) is applied. To disable any proxy, use option
``--no-proxy``:

::

    $ you-get --no-proxy 'http://www.youtube.com/watch?v=sGwy8DsUJ4M'

Watch a video in your media player of choice: (this is just a trick to
let you get rid of annoying ads on the video site)

::

    $ you-get -p vlc 'http://www.youtube.com/watch?v=sGwy8DsUJ4M'

FAQ
---

**Q**: Some videos on Youku are restricted to mainland China visitors.
Is it possible to bypass this restriction and download those videos?

**A**: Thanks to `Unblock
Youku <https://github.com/zhuzhuor/Unblock-Youku>`__, it is now possible
to access such videos from an oversea IP address. You can simply use
``you-get`` with option ``-y proxy.uku.im:8888``.

**Q**: Will you release an executable version / Windows Installer
package?

**A**: Yes, it's on my to-do list.

Command-Line Options
--------------------

For a complete list of available options, see:

::

    $ you-get --help
    Usage: you-get [OPTION]... [URL]...

    Startup options:
        -V | --version                           Display the version and exit.
        -h | --help                              Print this help and exit.

    Download options (use with URLs):
        -f | --force                             Force overwriting existed files.
        -i | --info                              Display the information of videos without downloading.
        -u | --url                               Display the real URLs of videos without downloading.
        -c | --cookies                           Load NetScape's cookies.txt file.
        -n | --no-merge                          Don't merge video parts.
        -F | --format <STREAM_ID>                Video format code.
        -o | --output-dir <PATH>                 Set the output directory for downloaded videos.
        -p | --player <PLAYER [options]>         Directly play the video with PLAYER like vlc/smplayer.
        -x | --http-proxy <HOST:PORT>            Use specific HTTP proxy for downloading.
        -y | --extractor-proxy <HOST:PORT>       Use specific HTTP proxy for extracting stream data.
             --no-proxy                          Don't use any proxy. (ignore $http_proxy)
             --debug                             Show traceback on KeyboardInterrupt.

License
-------

You-Get is licensed under the `MIT
license <https://raw.github.com/soimort/you-get/master/LICENSE.txt>`__.

Reporting an Issue / Contributing
---------------------------------

Please read
`CONTRIBUTING.md <https://github.com/soimort/you-get/blob/master/CONTRIBUTING.md>`__
first.

.. |Build Status| image:: https://api.travis-ci.org/soimort/you-get.png
   :target: https://travis-ci.org/soimort/you-get
.. |PyPI version| image:: https://badge.fury.io/py/you-get.png
   :target: http://badge.fury.io/py/you-get
.. |Gitter| image:: https://badges.gitter.im/Join%20Chat.svg
   :target: https://gitter.im/soimort/you-get?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge


Changelog
=========

0.3.35
------

*Date: 2015-09-21*

* New site support:
    - 755 http://7gogo.jp/ (via #659 by @soimort)
    - Funshion http://www.fun.tv/ (via #619 by @cnbeining)
    - iQilu http://v.iqilu.com/ (via #636 by @cnbeining)
    - Metacafe http://www.metacafe.com/ (via #620 by @cnbeining)
    - Qianmo http://qianmo.com/ (via #600 by @cnbeining)
    - Weibo Miaopai http://weibo.com/ (via #605 by @cnbeining)
* Bug fixes:
    - 163 (by @lilydjwg)
    - CNTV (by @Red54)
    - Dailymotion (by @jackyzy823 and @ddumitran)
    - iQIYI (by @jackyzy823 and others)
    - QQ (by @soimort)
    - SoundCloud (by @soimort)
    - Tudou (by @CzBiX)
    - Vimeo channel (by @cnbeining)
    - YinYueTai (by @soimort)
    - Youku (by @junzh0u)
    - Embedded Youku/Tudou player (by @zhangn1985)

0.3.34
------

*Date: 2015-07-12*

* Bug fix release

0.3.33
------

*Date: 2015-06-10*

* Many bug fixes by our awesome contributors

0.3.32
------

*Date: 2014-12-10*

* New site support:
    - baomihua.com
    - zhanqi.tv
* Bug fixes:
    - DouyuTV
    - Tudou
    - Tumblr
    - Vine
    - Youku

0.3.31
------

*Date: 2014-11-01*

* New site support:
    - Dongting (by @lilydjwg)
    - DouyuTV (by @0x00-pl)
    - LeTV cloud (by @cnbeining)
* Bug fixes:
    - AcFun
    - Bilibili
    - Niconico
    - iQIYI

0.3.30
------

*Date: 2014-09-21*

* First Alpha release
* Support PyPy3
* Bug fixes:
    - YouTube
    - Youku
    - Tudou
    - Niconico
    - AcFun

0.3.30dev-20140907
------------------

*Date: 2014-09-07*

* Bug fixes:
    - AcFun
    - iQIYI
    - MioMio
    - QQ

0.3.30dev-20140820
------------------

*Date: 2014-08-20*

* Bug fix release

0.3.30dev-20140812
------------------

*Date: 2014-08-12*

* Bug fixes:
    - Youku
* New site support:
    - VideoBam (by @cnbeining)

0.3.30dev-20140806
------------------

*Date: 2014-08-06*

* Bug fixes:
    - Youku
    - Nicovideo
    - Bilibili
    - Letv
* New site support:
    - Tucao.cc
* Use FFmpeg concat demuxer to join video segments (ffmpeg>=1.1)

0.3.30dev-20140730
------------------

*Date: 2014-07-30*

* YouTube: support fixed
* Youku: password-protected video support

0.3.30dev-20140723
------------------

*Date: 2014-07-23*

* YouTube: (experimental) video format selection
* Youku: playlist support
* NetEase Music: high quality download (by @farseer90718)
* PPTV: support fixed (by @jackyzy823)
* Catfun.tv: new site support (by @jackyzy823)
* AcFun.tv: domain name fixed

0.3.30dev-20140716
------------------

*Date: 2014-07-16*

* Bug fix release for:
    - YouTube
    - Youku

* New site support: (by @jackyzy823)
    - MTV 81 http://www.mtv81.com
    - Kugou (酷狗音乐) http://www.kugou.com
    - Kuwo (酷我音乐) http://www.kuwo.cn
    - NetEase Music (网易云音乐) http://music.163.com

0.3.30dev-20140629
------------------

*Date: 2014-06-29*

* Bug fix release for:
    - Youku
    - YouTube
    - TED
    - Bilibili
* (Experimental) Video format selection (for Youku only)

0.3.29
------

*Date: 2014-05-29*

* Bug fix release

0.3.28.3
--------

*Date: 2014-05-18*

* New site support:
    - CBS.com

0.3.28.2
--------

*Date: 2014-04-13*

* Bug fix release

0.3.28.1
--------

*Date: 2014-02-28*

* Bug fix release

0.3.28
------

*Date: 2014-02-21*

* New site support:
    - Magisto.com
    - VK.com

0.3.27
------

*Date: 2014-02-14*

* Bug fix release

0.3.26
------

*Date: 2014-02-08*

* New features:
    - Play video in players (#286)
    - LeTV support (#289)
    - Youku 1080P support
* Bug fixes:
    - YouTube (#282, #292)
    - Sina (#246, #280)
    - Mixcloud
    - NetEase
    - QQ
    - Vine

0.3.25
------

*Date: 2013-12-20*

* Bug fix release

0.3.24
------

*Date: 2013-10-30*

* Experimental: Sogou proxy server
* Fix issues for:
    - Vimeo

0.3.23
------

*Date: 2013-10-23*

* Support YouTube playlists
* Support general short URLs
* Fix issues for:
    - Sina

0.3.22
------

*Date: 2013-10-18*

* Fix issues for:
    - Baidu
    - Bilibili
    - JPopsuki TV
    - Niconico
    - PPTV
    - TED
    - Tumblr
    - YinYueTai
    - YouTube
    - ...

0.3.21
------

*Date: 2013-08-17*

* Fix issues for:
    - YouTube
    - YinYueTai
    - pan.baidu.com

0.3.20
------

*Date: 2013-08-16*

* Add support for:
    - eHow
    - Khan Academy
    - TED
    - 5sing
* Fix issues for:
    - Tudou

0.3.18
------

*Date: 2013-07-19*

* Fix issues for:
    - Dailymotion
    - Youku
    - Sina
    - AcFun
    - bilibili

0.3.17
------

*Date: 2013-07-12*

* Fix issues for:
    - YouTube
    - 163
    - bilibili
* Code cleanup.

0.3.16
------

*Date: 2013-06-28*

* Fix issues for:
    - YouTube
    - Sohu
    - Google+ (enable HTTPS proxy)

0.3.15
------

*Date: 2013-06-21*

* Add support for:
    - Instagram

0.3.14
------

*Date: 2013-06-14*

* Add support for:
    - Alive.in.th
* Remove support of:
    - JPopsuki
* Fix issues for:
    - AcFun
    - iQIYI

0.3.13
------

*Date: 2013-06-07*

* Add support for:
    - Baidu Wangpan (video only)
* Fix issue for:
    - Google+

0.3.12
------

*Date: 2013-05-19*

* Fix issues for:
    - Google+
    - Mixcloud
    - Tudou

0.3.11
------

*Date: 2013-04-26*

* Add support for:
    - Google Drive (Google Docs)

0.3.10
------

*Date: 2013-04-19*

* Add support for:
    - SongTaste
* Support Libav as well as FFmpeg.

0.3.9
-----

*Date: 2013-04-12*

* Add support for:
    - Freesound

0.3.8
-----

*Date: 2013-04-05*

* Add support for:
    - Coursera

0.3.7
-----

*Date: 2013-03-29*

* Add support for:
    - Baidu

0.3.6
-----

*Date: 2013-03-22*

* Add support for:
    - Vine
* Fix issue for:
    - YouTube

0.3.5
-----

*Date: 2013-03-15*

* Default to use FFmpeg for merging .flv files.

0.3.4
-----

*Date: 2013-03-08*

* Add support for:
    - Blip
    - VID48

0.3.3
-----

*Date: 2013-03-01*

* Add support for:
    - Douban
    - MioMio
* Fix issues for:
    - Tudou
    - Vimeo

0.3.2
-----

*Date: 2013-02-22*

* Add support for:
    - JPopsuki
* Fix issue for Xiami.

0.3.1
-----

*Date: 2013-02-15*

* Fix issues for Google+ and Mixcloud.
* API changed.

0.3.0
-----

*Date: 2013-02-08*

* Add support for:
    - Niconico

0.3dev-20130201
---------------

*Date: 2013-02-01*

* Add support for:
    - Mixcloud
    - Facebook
    - Joy.cn

0.3dev-20130125
---------------

*Date: 2013-01-25*

* Dailymotion: downloading best quality available now.
* iQIYI: fix `#77 <https://github.com/soimort/you-get/issues/77>`_.

0.3dev-20130118
---------------

*Date: 2013-01-18*

* YinYueTai: downloading best quality available now.
* Sohu: fix `#69 <https://github.com/soimort/you-get/issues/69>`_.

0.3dev-20130111
---------------

*Date: 2013-01-11*

* Add support for:
    - NetEase (v.163.com)
    - YouTube short URLs
* Vimeo: downloading best quality available now.

0.3dev-20130104
---------------

*Date: 2013-01-04*

* Sohu:
    - fix `#53 <https://github.com/soimort/you-get/issues/53>`_.
    - merge pull request `#54 <https://github.com/soimort/you-get/pull/54>`_; downloading best quality available now.

0.3dev-20121228
---------------

*Date: 2012-12-28*

* Add support for:
    - Xiami
    - Tumblr audios

0.3dev-20121221
---------------

*Date: 2012-12-21*

* YouTube: fix `#45 <https://github.com/soimort/you-get/issues/45>`_.
* Merge pull request `#46 <https://github.com/soimort/you-get/pull/46>`_; fix title parsing issue on Tudou.

0.3dev-20121220
---------------

*Date: 2012-12-20*

* YouTube: quick dirty fix to `#45 <https://github.com/soimort/you-get/issues/45>`_.

0.3dev-20121219
---------------

*Date: 2012-12-19*

* Add support for:
    - Tumblr

0.3dev-20121217
---------------

*Date: 2012-12-17*

* Google+: downloading best quality available now.
* Fix issues `#42 <https://github.com/soimort/you-get/issues/42>`_, `#43 <https://github.com/soimort/you-get/issues/43>`_ for Google+.
* Merge pull request `#40 <https://github.com/soimort/you-get/pull/40>`_; fix some issues for Ku6, Sina and 56.

0.3dev-20121212
---------------

*Date: 2012-12-12*

* YouTube: fix some major issues on parsing video titles.

0.3dev-20121210
---------------

*Date: 2012-12-10*

* YouTube: downloading best quality available now.
* Add support for:
    - SoundCloud

0.2.16
------

*Date: 2012-12-01*

* Add support for:
    - QQ
* Small fixes merged from youku-lixian.

0.2.15
------

*Date: 2012-11-30*

* Fix issue `#30 <https://github.com/soimort/you-get/issues/30>`_ for bilibili.

0.2.14
------

*Date: 2012-11-29*

* Fix issue `#28 <https://github.com/soimort/you-get/issues/28>`_ for Tudou.
* Better support for AcFun.

0.2.13
------

*Date: 2012-10-30*

* Nothing new.

0.2.12
------

*Date: 2012-10-30*

* Fix issue `#20 <https://github.com/soimort/you-get/issues/20>`_ for AcFun.

0.2.11
------

*Date: 2012-10-23*

* Move on to Python 3.3!
* Fix issues:
    - `#17 <https://github.com/soimort/you-get/issues/17>`_
    - `#18 <https://github.com/soimort/you-get/issues/18>`_
    - `#19 <https://github.com/soimort/you-get/issues/19>`_

0.2.10
------

*Date: 2012-10-16*

* Add support for:
    - Google+

0.2.9
-----

*Date: 2012-10-09*

* Fix issue `#16 <https://github.com/soimort/you-get/issues/16>`_.

0.2.8
-----

*Date: 2012-10-02*

* Fix issue `#15 <https://github.com/soimort/you-get/issues/15>`_ for AcFun.

0.2.7
-----

*Date: 2012-09-28*

* Fix issue `#6 <https://github.com/soimort/you-get/issues/6>`_ for YouTube.

0.2.6
-----

*Date: 2012-09-26*

* Fix issue `#5 <https://github.com/soimort/you-get/issues/5>`_ for YinYueTai.

0.2.5
-----

*Date: 2012-09-25*

* Add support for:
    - Dailymotion

0.2.4
-----

*Date: 2012-09-18*

* Use FFmpeg for converting and joining video files.
* Add '--url' and '--debug' options.

0.2.2
-----

*Date: 2012-09-17*

* Add danmaku support for AcFun and bilibili.
* Fix issue `#2 <https://github.com/soimort/you-get/issues/2>`_ and `#4 <https://github.com/soimort/you-get/issues/4>`_ for YouTube.
* Temporarily fix issue for iQIYI (use .ts instead of .f4v).

0.2.1
-----

*Date: 2012-09-02*

* Add support for:
    - ifeng

0.2
---

*Date: 2012-09-02*

* Add support for:
    - Vimeo
    - AcFun
    - bilibili
    - CNTV
    - iQIYI
    - Ku6
    - PPTV
    - Sina
    - Sohu
    - 56

0.1.3
-----

*Date: 2012-09-01*

* Playlist URLs are now automatically handled. ('--playlist' option is no longer needed)
* Handle KeyboardInterrupt silently.
* Fix Unicode character display on code pages.

0.1
---

*Date: 2012-09-01*

* First PyPI release.
* Fix issue `#1 <https://github.com/soimort/you-get/issues/1>`_.

0.0.1
-----

*Date: 2012-08-21*

* Initial release, forked from `iambus/youku-lixian <https://github.com/iambus/youku-lixian>`_; add:
    - YouTube support.
    - Pausing and resuming of downloads.
    - HTTP proxy settings.


