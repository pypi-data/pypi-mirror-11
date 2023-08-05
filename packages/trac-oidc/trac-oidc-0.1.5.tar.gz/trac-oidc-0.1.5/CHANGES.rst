*******
History
*******

0.1.5 (2015-07-16)
==================

- If the stock ``trac.web.auth.LoginModule`` is disabled, then handle
  requests for ``/login`` too (because no one else is going to.)

0.1.4 (2015-06-24)
==================

Features
~~~~~~~~

- Tests now run under trac 1.1.5

0.1.3 (2015-06-23)
==================

Behavioral Changes
~~~~~~~~~~~~~~~~~~

- In the "logged in as %(user)s" message (in the *metanav* menu),
  *user* is now always set to the *session id* (also referred to as the
  *authname*) of the logged-in user.  Previously the real name of the
  user was shown instead, when it was available.  This now matches the
  behavior of the stock ``LoginModule`` component.

Bugs Fixed
~~~~~~~~~~

- The *Logout* link should now work again.  It was broken for trac >= 1.0.2.

Large Refactor
~~~~~~~~~~~~~~

- Lots of code cleanup, including splitting of logic into several
  components/classes, include:

  - ``AuthCookieManager``: for managing the trac authentication cookie

  - ``UserDatabase``: for mapping between *OpenID identities* and trac
    *authname*\s.

  - ``SessionHelper``: for searching and managing authenticated sessions

  - ``Authenticator``: for handling the *OpenID Connect* flow

0.1.2 (2015-06-20)
==================

Features
~~~~~~~~

- The plugin should now work with trac 0.11.

Bugs Fixed
~~~~~~~~~~

- [trac > 1.0.2] Fixed *Logout* link so that it works under trac >
  1.0.2.  Recent tracs use a logout form rather than a link (for CSRF
  protection.)

Testing
~~~~~~~

- Added a functional test.  Run tests with trac version 0.11, 0.12 and
  latest (1.0).

Refactor
~~~~~~~~

- Renamed ``trac_oidc.plugin`` module to ``trac_oidc.trac_oidc``.
  Trac’s default log format string includes ``"[%(module)s]"`` —
  ``[trac_oidc]`` is much more informative than ``[plugin]``.


0.1.1 (2015-06-18)
==================

Initial release.  There is no 0.1 (I botched the upload to PyPI).
