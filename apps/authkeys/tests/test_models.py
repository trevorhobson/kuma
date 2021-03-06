from django.contrib.auth.models import User

from django.test import TestCase

from nose.tools import ok_
from nose.plugins.attrib import attr

from authkeys.models import Key


class KeyViewsTest(TestCase):

    def setUp(self):
        self.user = User(username="tester23",
                         email="tester23@example.com")
        self.user.save()

    def tearDown(self):
        self.user.delete()

    @attr('current')
    def test_secret_generation(self):
        """Generated secret should be saved as a hash and pass a check"""
        key = Key(user=self.user)
        secret = key.generate_secret()
        key.save()
        ok_(key.key)
        ok_(key.hashed_secret)
        ok_(len(key.hashed_secret) > 0)
        ok_(len(secret) > 0)
        ok_(secret != key.hashed_secret)
        ok_(not key.check_secret("I AM A FAKE"))
        ok_(key.check_secret(secret))
