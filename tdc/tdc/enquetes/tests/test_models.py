from django import test
from django.db import models as django_models

from tdc.enquetes import models


class EnqueteTestCase(test.TestCase):

    def test_deve_ter_titulo(self):
        campo = models.Enquete._meta.get_field_by_name("titulo")[0]
        self.assertIsInstance(campo, django_models.CharField)
        self.assertEqual(100, campo.max_length)

    def test_deve_ter_descricao(self):
        campo = models.Enquete._meta.get_field_by_name("descricao")[0]
        self.assertIsInstance(campo, django_models.CharField)
        self.assertEqual(1000, campo.max_length)


class OpcaoTestCase(test.TestCase):
    def test_deve_ter_titulo(self):
        campo = models.Opcao._meta.get_field_by_name("titulo")[0]
        self.assertIsInstance(campo, django_models.CharField)
        self.assertEqual(100, campo.max_length)

    def test_deve_referenciar_enquete(self):
        campo = models.Opcao._meta.get_field_by_name("enquete")[0]
        self.assertIsInstance(campo, django_models.ForeignKey)
        self.assertEqual(models.Enquete, campo.related.parent_model)


class VotoTestCase(test.TestCase):
    def test_deve_referenciar_opcao(self):
        campo = models.Voto._meta.get_field_by_name("opcao")[0]
        self.assertIsInstance(campo, django_models.ForeignKey)
        self.assertEqual(models.Opcao, campo.related.parent_model)

    def test_deve_ter_data(self):
        campo = models.Voto._meta.get_field_by_name("data")[0]
        self.assertIsInstance(campo, django_models.DateTimeField)
        self.assertTrue(campo.auto_now_add)
