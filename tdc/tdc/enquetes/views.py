# coding: utf-8

from django import http, shortcuts
from django.template import response
from django.views.generic import base

from tdc.enquetes import models


class EnqueteView(base.View):

    def get(self, request, *args, **kwargs):
        enquete = shortcuts.get_object_or_404(models.Enquete,
                                              id=kwargs["id"])
        ctx = kwargs.get("contexto", {})
        ctx["enquete"] = enquete
        return response.TemplateResponse(request,
                                         "enquete.html",
                                         ctx)

    def post(self, request, *args, **kwargs):
        opcao_id = request.POST.get("opcao")
        if not opcao_id:
            kwargs["contexto"] = {"erro": u"Por favor, escolha uma opção."}
            return self.get(request, *args, **kwargs)
        opcao = shortcuts.get_object_or_404(models.Opcao,
                                            id=opcao_id,
                                            enquete=kwargs["id"])
        models.Voto.objects.create(opcao=opcao)
        return http.HttpResponse("voto computado")
