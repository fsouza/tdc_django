# Create your views here.
from django import http, shortcuts
from django.template import response
from django.views.generic import base

from tdc.enquetes import models


class EnqueteView(base.View):

    def get(self, request, *args, **kwargs):
        enquete = shortcuts.get_object_or_404(models.Enquete,
                                              id=kwargs["id"])
        return response.TemplateResponse(request,
                                         "enquete.html",
                                         {"enquete": enquete})

    def post(self, request, *args, **kwargs):
        opcao = shortcuts.get_object_or_404(models.Opcao,
                                            id=request.POST["opcao"],
                                            enquete=kwargs["id"])
        models.Voto.objects.create(opcao=opcao)
        return http.HttpResponse("voto computado")
