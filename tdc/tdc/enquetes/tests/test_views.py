from django import http, test
from django.template import response
from django.test import client

from tdc.enquetes import models, views


class EnqueteTestCase(test.TestCase):

    def setUp(self):
        self.enquete = models.Enquete.objects.create(
            titulo=u"Qual sua linguagem preferida?",
            descricao=u"Escolhe ae",
        )
        self.opcoes = models.Opcao.objects.bulk_create([
            models.Opcao(enquete=self.enquete, titulo=u"Java"),
            models.Opcao(enquete=self.enquete, titulo=u"C++"),
            models.Opcao(enquete=self.enquete, titulo=u"Ruby"),
            models.Opcao(enquete=self.enquete, titulo=u"Python"),
        ])

    def tearDown(self):
        models.Opcao.objects.filter(enquete=self.enquete).delete()
        self.enquete.delete()

    def test_deve_renderizar_template_com_enquete_no_contexto(self):
        factory = client.RequestFactory()
        request = factory.get("/enquetes/%d" % self.enquete.id)
        view = views.EnqueteView()
        resp = view.dispatch(request, id=self.enquete.id)
        self.assertIsInstance(resp, response.TemplateResponse)
        self.assertEqual("enquete.html", resp.template_name)
        self.assertEqual(self.enquete, resp.context_data["enquete"])

    def test_deve_retornar_404_quando_a_enquete_nao_existe(self):
        factory = client.RequestFactory()
        request = factory.get("/enquetes/%d" % (self.enquete.id + 1))
        view = views.EnqueteView()
        with self.assertRaises(http.Http404):
            view.dispatch(request, id=self.enquete.id + 1)
