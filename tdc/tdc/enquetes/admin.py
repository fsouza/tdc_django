from django.contrib import admin
from tdc.enquetes import models


class OpcaoInline(admin.StackedInline):
    model = models.Opcao

admin.site.register(models.Enquete)
