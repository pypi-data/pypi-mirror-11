======================
django-secure-js-login
======================

JavaScript Challenge-handshake authentication django app.

+-----------------------------------+------------------------------------------------------------+
| |Build Status on travis-ci.org|   | `travis-ci.org/jedie/django-secure-js-login`_              |
+-----------------------------------+------------------------------------------------------------+
| |Coverage Status on coveralls.io| | `coveralls.io/r/jedie/django-secure-js-login`_             |
+-----------------------------------+------------------------------------------------------------+
| |Status on landscape.io|          | `landscape.io/github/jedie/django-secure-js-login/master`_ |
+-----------------------------------+------------------------------------------------------------+

.. |Build Status on travis-ci.org| image:: https://travis-ci.org/jedie/django-secure-js-login.svg
.. _travis-ci.org/jedie/django-secure-js-login: https://travis-ci.org/jedie/django-secure-js-login/
.. |Coverage Status on coveralls.io| image:: https://coveralls.io/repos/jedie/django-secure-js-login/badge.svg
.. _coveralls.io/r/jedie/django-secure-js-login: https://coveralls.io/r/jedie/django-secure-js-login
.. |Status on landscape.io| image:: https://landscape.io/github/jedie/django-secure-js-login/master/landscape.svg
.. _landscape.io/github/jedie/django-secure-js-login/master: https://landscape.io/github/jedie/django-secure-js-login/master

First:
The Secure-JS-Login is not a simple *"send username + PBKDF2-SHA(password)"*
It is more a `Challenge-handshake authentication protocol <http://en.wikipedia.org/wiki/Challenge-handshake_authentication_protocol>`_!

------
Status
------

Current implementation used the new Web Cryptography API:

* PBKDF2, deriveBits with SHA-1

So, not every browser/OS combination will work.

Just try `https://diafygi.github.io/webcrypto-examples/ <https://diafygi.github.io/webcrypto-examples/>`_ with your preferred browser/OS.

Some browser information's:

**Firefox** support everything in "newer" version.
The `MDN Window.crypto <https://developer.mozilla.org/en-US/docs/Web/API/Window/crypto>`_ page doesn't contains a minimum version number.
e.g.: **v31.0esr** doesn't support crypto. **v38.0esr** is needed.

Google **chrome** and **Chromium** is not supported on platforms using NSS for their crypto (Linux and ChromeOS).
So on Windows is may work, but not tested, yet.
This will be solved in future versions of Chrome, see also: `https://www.chromium.org/blink/webcrypto <https://www.chromium.org/blink/webcrypto>`_
...and it seems that WebCrypt is only available with **https**, see:
`https://www.chromium.org/Home/chromium-security/prefer-secure-origins-for-powerful-new-features <https://www.chromium.org/Home/chromium-security/prefer-secure-origins-for-powerful-new-features>`_

Apple **Safari** should be supported, but not tested, yet.

**IE11** has window.msCrypto but doesn't provide promise ``.then()`` / ``.catch()``
It used the outdated ``.oncomplete()`` / ``.onerror()``
Maybe a work-a-round is possible. Pull request are welcome ;)
The new **Edge** browser in Windows 10 maybe supported.

Time-based One-time Password (TOTP)
===================================

Optional: Two-way verification with Time-based One-time Password (TOTP) specified in `RFC 6238 <https://tools.ietf.org/html/rfc6238>`_.

Clients, e.g:

* `https://github.com/google/google-authenticator <https://github.com/google/google-authenticator>`_

* `https://github.com/markmcavoy/androidtoken <https://github.com/markmcavoy/androidtoken>`_

Python Packages used:

* `https://pypi.python.org/pypi/django-otp <https://pypi.python.org/pypi/django-otp>`_

* `https://pypi.python.org/pypi/PyQRCode <https://pypi.python.org/pypi/PyQRCode>`_

------------------------------
switch from PBKDF2 to scrypt ?
------------------------------

existing solutions:

`https://pypi.python.org/pypi/django-scrypt/ <https://pypi.python.org/pypi/django-scrypt/>`_ that used `https://pypi.python.org/pypi/scrypt/ <https://pypi.python.org/pypi/scrypt/>`_

But both projects sleeps?

--------------
The procedure:
--------------

Save a new user password:
=========================

client browser / JavaScript part::

#. user input a password

#. ``init_pbkdf2_salt = SHA1(random data)``

#. ``pbkdf2_hash = pbkdf2("Plain Password", salt=init_pbkdf2_salt)``

#. Client send **init_pbkdf2_salt** and **pbkdf2_hash** to the server

Server part:

#. Server split **pbkdf2_hash** into: **first_pbkdf2_part** and **second_pbkdf2_part**

#. ``encrypted_part = xor_encrypt(first_pbkdf2_part, key=second_pbkdf2_part)``

#. Save only **encrypted_part** and given **init_pbkdf2_salt** from client

Login - client browser / JavaScript part:
=========================================

#. Use request login

#. server send html login form with a random **server_challenge** value

#. User enters his **username** and **password**

#. Ajax Request the **init_pbkdf2_salt** from server with the given **username**

#. generate the auth data:

    #. ``pbkdf2_temp_hash = pbkdf2("Plain Password", init_pbkdf2_salt)``

    #. split **pbkdf2_temp_hash** into **first_pbkdf2_part** and **second_pbkdf2_part**

    #. ``cnonce = SHA512(random data)``

    #. ``pbkdf2_hash = pbkdf2(first_pbkdf2_part, salt=cnonce + server_challenge)``

#. send **pbkdf2_hash**, **second_pbkdf2_part** and **cnonce** to the server

validation on the server
------------------------

#. client POST data: **pbkdf2_hash**, **second_pbkdf2_part** and **cnonce**

#. get transmitted **server_challenge** value from session

#. get **encrypted_part** and **salt** from database via given **username**

#. ``first_pbkdf2_part = xor_decrypt(encrypted_part, key=second_pbkdf2_part)``

#. ``test_hash = pbkdf2(first_pbkdf2_part, key=cnonce + server_challenge)``

#. compare **test_hash** with transmitted **pbkdf2_hash**

secure?
=======

Secure-JS-Login is not really secure in comparison to https! e.g. the client can't validate if he really communicate with the server or with a `Man-in-the-middle attack <https://en.wikipedia.org/wiki/Man-in-the-middle_attack>`_.

However the used procedure is safer than plain-text authentication. In addition, on the server no plain-text passwords are stored. With the data that are stored on the server, can not be used alone.

If you have `https <http://en.wikipedia.org/wiki/HTTPS>`_, you can combine it with Secure-JS-Login, similar to combine a digest auth with https.

More information: `Warum Secure-JS-Login Sinn macht... <http://www.pylucid.org/permalink/35/warum-js-sha-login-sinn-macht>`_ (german only, sorry)

why?
====

Many, if not even all CMS/wiki/forum, used unsecure Login. User name and password send in **plaintext** over the Internet. A reliable solution offers only `https`_.

The Problem: No Provider offers secured HTTP connection for little money :(

alternative solutions
=====================

* `Digest access authentication <http://en.wikipedia.org/wiki/Digest_access_authentication>`_ (implementation in django exist: `django-digest <http://bitbucket.org/akoha/django-digest/wiki/Home>`_):

    * pro

        * Browser implemented it, so no additional JavaScript needed

    * cons

        * Password hash must be saved on the server, without any salt! The hash can be used for login, because: ``hash = MD5(username:realm:password)``

        * used old MD5 hash

------
tryout
------

e.g.:

::

    ~ $ virtualenv secure-js-login-env
    ~ $ cd secure-js-login-env
    ~/secure-js-login-env $ source bin/activate

    # install secure-js-login as "editable" to have access to example project server and unittests:

    (secure-js-login-env)~/secure-js-login-env $ pip install -e git+git://github.com/jedie/django-secure-js-login.git#egg=django-secure-js-login

    run example project server:
    {{{
    (secure-js-login-env)~/secure-js-login-env $ cd src/django-secure-js-login/
    (secure-js-login-env)~/secure-js-login-env/src/django-secure-js-login $ ./run_example_server.sh

**Note:**
The `example_project <https://github.com/jedie/django-secure-js-login/tree/master/example_project>`_ is only for local tests!
It's insecure configured and used some hacks!

run inittests:

::

    (secure-js-login-env)~/secure-js-login-env/src/django-secure-js-login $ ./runtests.py

to run the Live-Server-Tests, install `selenium <https://pypi.python.org/pypi/selenium>`_ e.g.:

::

    (secure-js-login-env)~/secure-js-login-env/src/django-secure-js-login $ pip install selenium
    (secure-js-login-env)~/secure-js-login-env/src/django-secure-js-login $ ./runtests.py

-------
signals
-------

On every failed Secure-JS-Login a signal will be send.
To use this signal, e.g.:

::

    import sys
    from secure_js_login.signals import secure_js_login_failed

    def log_failed_login_handler(sender, reason, **kwargs):
        """ Just print the reason to stderr """
        print("Secure-JS-Login failed: %s" % reason, file=sys.stderr)

    secure_js_login_failed.connect(log_failed_login_handler)

-----
usage
-----

**settings.py**:

::

    INSTALLED_APPS = (
        #...
        "secure_js_login.honypot",
        "secure_js_login",
    )

    AUTHENTICATION_BACKENDS=(
        'secure_js_login.auth_backends.SecureLoginAuthBackend',
        'django.contrib.auth.backends.ModelBackend',
        #...
    )

    DEBUG=False # Otherwise the user will see detailed information if login failed!

    # use 'User.set_password' monkey-patch in models.py for create password hashes:
    AUTO_CREATE_PASSWORD_HASH = True

**urls.py**:

::

    from secure_js_login.honypot.urls import urls as honypot_urls
    from secure_js_login.urls import urls as secure_js_login_urls

    urlpatterns = i18n_patterns('',
        #...
        url(r'^login/', include(honypot_urls)),
        url(r'^secure_login/', include(secure_js_login_urls)),
        url(r'^jsi18n/(?P<packages>\S+?)/$', 'django.views.i18n.javascript_catalog'),
        #...
    )

Complete example: `example_project/urls.py <https://github.com/jedie/django-secure-js-login/blob/master/example_project/example_project/urls.py>`_

**templates**:

::

    <a href="{% url 'secure-js-login:login' %}">secure JS login</a>
    <a href="{% url 'honypot-login:login' %}">honypot login</a>

More interesting example:

::

    <a href="{% url 'honypot-login:login' %}" rel="nofollow" onclick="window.location.href = '{% url 'secure-js-login:login' %}'; return false;">login</a>

After adding secure-js-login create his tables with:

::

    .../your/page $ ./manage.py migrate

**Important:** The secure login will only work, if the user password was set **after** adding 'secure_js_login' to your project!

Troubleshooting
===============

logging/debug information
-------------------------

Turn on **settings.DEBUG** to see detailed error messages on failed login.

You can also use `logging <https://docs.djangoproject.com/en/1.7/topics/logging/>`_.
The app will use the logger name **secure_js_login**, e.g.:

::

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'file': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename': 'secure_js_login.log',
            },
        },
        'loggers': {
            'secure_js_login': {
                'handlers': ['file'],
                'level': 'DEBUG',
                'propagate': True,
            },
        },
    }

A console logging example can be found here: `example_project/settings.py <https://github.com/jedie/django-secure-js-login/blob/master/example_project/example_project/settings.py>`_

After login: 404 or redirect to "/accounts/profile/"
----------------------------------------------------

You didn't change the default `settings.LOGIN_REDIRECT_URL <https://docs.djangoproject.com/en/1.7/ref/settings/#login-redirect-url>`_

Login error: "Profile for user 'YourUsername' doesn't exists!"
--------------------------------------------------------------

The user exist, but the password was not set **after** adding 'secure_js_login' to your project!
Just change the user password. e.g.: on console:

::

    .../your/page $ ./manage.py changepassword YourUsername

...or use the normal django admin login and set the password there.

Login error: "authenticate() check failed."
-------------------------------------------

Check, if you add **'secure_js_login.auth_backends.SecureLoginAuthBackend'** to **AUTHENTICATION_BACKENDS**, see above!

---------------------
Version compatibility
---------------------

+-----------------+------------+------------+
| secure-js-login | Django     | Python     |
+=================+============+============+
| >=v0.1.0        | v1.7, v1.8 | v2.7, v3.4 |
+-----------------+------------+------------+

(These are the unittests variants. See `.travis.yml <https://github.com/jedie/django-secure-js-login/blob/master/.travis.yml>`_, maybe other versions are compatible, too.)

---------
changelog
---------

* v0.3.alpha0 - 26.7.2015

    * use Browser Web Cryptography API (instead of pure JavaScript SHA/PBKDF2 implementation)

    * Add optional: Two-way verification with Time-based One-time Password (TOTP) specified in RFC 6238.

    * increase default PBKDF2 iteration (TODO: test on Raspberry Pi 1 !)

    * check cnonce against replay attacks

    * refactor validation process

    * fire signal on failed login with a 'reason' message

    * Display detailed form errors, if settings.DEBUG is on else: only a common message

* v0.2.0 - 10.05.2015:

    * increase default PBKDF2 iteration after test on a Raspberry Pi 1

    * more unitests

    * Honypot login raise "normal" form errors

    * code cleanup

    * Docu update

* v0.1.0 - 06.05.2015:

    * initial release as reuseable app

    * Use PBKDF2 (pure JavaScript Implementation)

* 03.05.2015:

    * Split from `PyLucid CMS 'auth' plugin <https://github.com/jedie/PyLucid/tree/7ee6f8312e7ade65ff3604eb9eab810c26c43ccb/pylucid_project/pylucid_plugins/auth>`_

* 03.2010:

    * `Use ajax request via jQuery <http://www.python-forum.de/viewtopic.php?p=163746#p163746>`_ (de)

* 11.07.2007:

    * `New SHA challenge response procedure <http://www.python-forum.de/viewtopic.php?p=72926#p72926>`_ (de)

* 01.06.2005:

    * `first implementation of a MD5 login in PyLucid <http://www.python-forum.de/viewtopic.php?f=5&t=3345>`_ (de)

----------
info links
----------

* Python-Forum Threads (de):

    * `Digest auth als Alternative? <http://www.python-forum.de/viewtopic.php?f=7&t=22163>`_ (03.2010)

    * `Sinn oder Unsinn des PyLucids Secure-JS-Login... <http://www.python-forum.de/viewtopic.php?f=3&t=8180>`_ (12.2006)

    * `Wie Session-Hijacking verhindern? <http://www.python-forum.de/topic-8182.html>`_ (12.2006)

* `Diskussion auf de.comp.lang.python <https://groups.google.com/forum/#!topic/de.comp.lang.python/jAbfc26Bg_k>`_ (08.2006)

-------------
project links
-------------

+-----------------+---------------------------------------------------------+
| Github          | `https://github.com/jedie/django-secure-js-login`_      |
+-----------------+---------------------------------------------------------+
| Python Packages | `https://pypi.python.org/pypi/django-secure-js-login/`_ |
+-----------------+---------------------------------------------------------+
| Travis CI       | `https://travis-ci.org/jedie/django-secure-js-login/`_  |
+-----------------+---------------------------------------------------------+
| Coveralls       | `https://coveralls.io/r/jedie/django-secure-js-login`_  |
+-----------------+---------------------------------------------------------+

.. _https://github.com/jedie/django-secure-js-login: https://github.com/jedie/django-secure-js-login
.. _https://pypi.python.org/pypi/django-secure-js-login/: https://pypi.python.org/pypi/django-secure-js-login/
.. _https://travis-ci.org/jedie/django-secure-js-login/: https://travis-ci.org/jedie/django-secure-js-login/
.. _https://coveralls.io/r/jedie/django-secure-js-login: https://coveralls.io/r/jedie/django-secure-js-login

-------
contact
-------

Come into the conversation, besides the github communication features:

+---------+--------------------------------------------------------+
| IRC     | #pylucid on freenode.net (Yes, the PyLucid channel...) |
+---------+--------------------------------------------------------+
| webchat | `http://webchat.freenode.net/?channels=pylucid`_       |
+---------+--------------------------------------------------------+

.. _http://webchat.freenode.net/?channels=pylucid: http://webchat.freenode.net/?channels=pylucid

--------
donation
--------

* `Flattr This! <https://flattr.com/submit/auto?uid=jedie&url=https%3A%2F%2Fgithub.com%2Fjedie%2Fdjango-secure-js-login%2F>`_

* Send `Bitcoins <http://www.bitcoin.org/>`_ to `1823RZ5Md1Q2X5aSXRC5LRPcYdveCiVX6F <https://blockexplorer.com/address/1823RZ5Md1Q2X5aSXRC5LRPcYdveCiVX6F>`_

