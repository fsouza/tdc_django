from django import test
from django.contrib import admin as django_admin

from tdc.enquetes import models

django_admin.autodiscover()


class EnqueteTestCase(test.TestCase):

    def test_deve_estar_registrada(self):
        registry = django_admin.site._registry
        self.assertIn(models.Enquete, registry)
