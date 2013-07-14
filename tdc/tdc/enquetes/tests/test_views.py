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

    def test_deve_registrar_voto_no_POST(self):
        opcao = self.enquete.opcao_set.all()[0].pk
        dados = {"opcao": opcao}
        request = test.RequestFactory().post("/enquetes/{0}".format(self.enquete.pk),
                                             dados)
        resp = views.EnqueteView().dispatch(request, id=self.enquete.pk)
        self.assertEqual(200, resp.status_code)
        models.Voto.objects.get(opcao=opcao)

    def test_deve_retornar_404_quando_opcao_nao_existe(self):
        dados = {"opcao": 500}
        request = test.RequestFactory().post("/enquetes/{0}".format(self.enquete.pk),
                                             dados)
        with self.assertRaises(http.Http404):
            views.EnqueteView().dispatch(request, id=self.enquete.pk)

    def test_deve_retornar_404_quando_opcao_nao_eh_da_enquete(self):
        enquete = models.Enquete.objects.create(
            titulo=u"O que vc achou do TDC 2013?",
            descricao=u"queremos ouvir vc",
        )
        opcao = models.Opcao.objects.create(titulo="Muito bom", enquete=enquete)
        dados = {"opcao": opcao.pk}
        request = test.RequestFactory().post("/enquetes/{0}".format(self.enquete.pk),
                                             dados)
        with self.assertRaises(http.Http404):
            views.EnqueteView().dispatch(request, id=self.enquete.pk)
