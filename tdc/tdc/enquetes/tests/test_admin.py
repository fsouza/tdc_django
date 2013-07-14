from django import test
from django.contrib import admin as django_admin

from tdc.enquetes import admin, models

django_admin.autodiscover()


class EnqueteTestCase(test.TestCase):

    def test_deve_estar_registrada(self):
        registry = django_admin.site._registry
        self.assertIn(models.Enquete, registry)


class OpcaoInlinceTestCase(test.TestCase):

    def test_deve_ser_stacked(self):
        assert issubclass(admin.OpcaoInline, django_admin.StackedInline)

    def test_model_deve_ser_Opcao(self):
        self.assertEqual(models.Opcao, admin.OpcaoInline.model)
