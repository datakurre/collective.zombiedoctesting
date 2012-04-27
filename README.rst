Fast functional JavaScript testing with Zombie.js
=================================================

Zombie.js_ is a fast headless browser with all the JavaScript support Node.js_
provides. This package provides a function decorator, which allows Python
doctest-style functional JavaScript testing using Python-like CoffeeScript.

**Disclaimer:** This is mostly an experiment. This wouldn't ever replace your
existing Selenium-stack, because Zombie.js, even when it works, is just an
another browser with its own quirks.

.. _Zombie.js: http://zombie.labnotes.org/
.. _Node.js: http://nodejs.org/


Requirements
------------

- a UNIX like environment
- Node.js_ must be installed
- npm_ must be installed
- ``coffee-script``, ``zombie`` and ``async`` packages must be installed using
  npm
- ``coffee``-executable must be found on the path

.. _npm: http://npmjs.org/

The requirements should be filled, when you can run the following command on a
console without it printing anything (returning any errors)::

    $ echo "require 'zombie'; require 'async'"|coffee -s


Example of use (with ``plone.app.testing``)
-------------------------------------------

Start with defining a functional testing fixture with ZServer (that will run
your Plone on localhost:55001 by default)::

    from plone.app.testing import PLONE_FIXTURE
    from plone.app.testing import FunctionalTesting

    from plone.testing import z2

    FUNCTIONAL_TESTING = FunctionalTesting(
        bases=(PLONE_FIXTURE, z2.ZSERVER_FIXTURE), name="PloneFixture:ZServer")


Then write your functional JavaScript test as a doctest for your testmethod
using CoffeeScript instead of Python. Define the context (URL) of your test by
using the decorator (``@browser``) from ``collective.zombiedoctesting`` as
shown below. You may use all the JavaScript that's provided by your context and
the global ``browser`` that represents Zombie.js' browser::

    import unittest

    from plone.app.testing import TEST_USER_NAME
    from plone.app.testing import TEST_USER_PASSWORD

    from collective.zombiedoctesting import browser

    constants = {
        "TEST_USER_NAME": TEST_USER_NAME,
        "TEST_USER_PASSWORD": TEST_USER_PASSWORD
        }


    class LoginOverlayTest(unittest.TestCase):

        layer = FUNCTIONAL_TESTING

        @browser("http://localhost:55001/plone/", mapping=constants)
        def test_login(self):
            """
            Let's start by looking up the login link using the jQuery available
            on our site:

            >>> console.log $("#personaltools-login").text()
            Log in

            Clicking that link should not redirect us anywhere, but give us an
            AJAX overlay with a login form.

            >>> $("#personaltools-login").click()
            >>> console.log window.location.href
            ... console.log $(".pb-ajax #login-form").text()
            http://localhost:55001/plone/
            Login Name
            Password

            Let's store that form as global (to be available between different
            doctest examples) and fill it...

            >>> global.form = $(".pb-ajax #login-form")
            ... form.find("#__ac_name").val("%(TEST_USER_NAME)s")
            ... form.find("#__ac_password").val("%(TEST_USER_PASSWORD)s")
            ... console.log form.find("#__ac_name").val()
            ... console.log form.find("#__ac_password").val()
            %(TEST_USER_NAME)s
            %(TEST_USER_PASSWORD)s

            ... and click the button to log in.

            >>> form.find("input[type='submit']").click()
            >>> console.log window.location.href
            ... console.log browser.text(".documentFirstHeading")
            http://localhost:55001/plone/login_form
            You are now logged in

            Uh oh, we were properly logged in, but we were redirected also, so
            zombie is not a perfect browser yet.

            Also, notice, that we couldn't use jQuery in testing the document
            first heading (we used zombie's custom browser API), because the
            context after the click is an AJAX-response without jQuery or any
            other javascript.
            """

Note that every parsed doctest-example (a line starting with *>>>*) is executed
separately, but you may use Node.js' ``global`` to make variables available
between doctest-examples.

If you'd like to see the complete JavaScript generated to be run with zombie,
you may add ``debug=True`` into ``@browser``-decorator call.
