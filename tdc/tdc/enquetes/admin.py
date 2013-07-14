from django.contrib import admin
from tdc.enquetes import models


class OpcaoInline(admin.StackedInline):
    model = models.Opcao


class EnqueteAdmin(admin.ModelAdmin):
    inlines = [OpcaoInline]

admin.site.register(models.Enquete, EnqueteAdmin)
