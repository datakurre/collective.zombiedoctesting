Fast functional JavaScript testing with Zombie.js
=================================================

Zombie.js_ is a fast headless browser with all the JavaScript support Node.js
provides. This is package provides a function decorator, which allows Python
doctest-style functional JavaScript testing using Python-like CoffeeScript.

Disclaimer: This may not replace your Selenium-stack, because Zombie.js is just
an another browser with its own quirks.

.. _Zombie.js: http://zombie.labnotes.org/

Requirements
------------

- Node.js must be installed
- npm must be installed
- coffeescript, zombiejs and async packages must be installed using npm
- coffee-executable must be found on the path


Example of use (with ``plone.app.testing``)
-------------------------------------------

Start with defining a functional testing fixture with ZServer (that will run
your Plone on localhost:55001 by default)::

    from plone.app.testing import PLONE_FIXTURE
    from plone.app.testing import FunctionalTesting

    from plone.testing import z2

    FUNCTIONAL_TESTING = FunctionalTesting(
        bases=(PLONE_FIXTURE, z2.ZSERVER_FIXTURE), name="PloneFixture:ZServer")


Then write your functional JavaScript tests as a doctest for your testmethod
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
            Let's start by looking up the login link.

            >>> console.log do $("#personaltools-login").text
            Log in

            Clicking that link should not redirect us anywhere, but give us an
            AJAX overlay with a login form.

            >>> do ($ "#personaltools-login").click
            >>> console.log window.location.href
            ... console.log do ($ ".pb-ajax #login-form").text
            http://localhost:55001/plone/
            Login Name
            Password

            Let's fill that form...

            >>> global.form = ($ ".pb-ajax #login-form")
            ... form.find("#__ac_name").val "%(TEST_USER_NAME)s"
            ... form.find("#__ac_password").val "%(TEST_USER_PASSWORD)s"
            ... console.log do form.find("#__ac_name").val
            ... console.log do form.find("#__ac_password").val
            %(TEST_USER_NAME)s
            %(TEST_USER_PASSWORD)s

            ... and click the button to log in.

            >>> do form.find("input[type='submit']").click
            >>> console.log window.location.href
            ... console.log browser.text ".documentFirstHeading"
            http://localhost:55001/plone/login_form
            You are now logged in
            """
