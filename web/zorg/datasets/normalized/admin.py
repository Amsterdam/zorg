from django.contrib import admin
from .models import Locatie, Organisatie, Activiteit


class LocatieAdmin(admin.ModelAdmin):
    pass


class OrganisatieAdmin(admin.ModelAdmin):
    pass


class ActiviteitAdmin(admin.ModelAdmin):
    pass

admin.site.register(Locatie, LocatieAdmin)
admin.site.register(Organisatie, OrganisatieAdmin)
admin.site.register(Activiteit, ActiviteitAdmin)
