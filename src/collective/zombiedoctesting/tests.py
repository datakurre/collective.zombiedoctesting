# -*- coding: utf-8 -*-
"""An example test case for Plone"""

from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import FunctionalTesting

from plone.testing import z2

FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(PLONE_FIXTURE, z2.ZSERVER_FIXTURE), name="PloneFixture:ZServer")


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
