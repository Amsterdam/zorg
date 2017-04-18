from django.contrib import admin
from .models import Locatie, Organisatie, Activiteit, Persoon, Profile


class LocatieAdmin(admin.ModelAdmin):
    pass


class OrganisatieAdmin(admin.ModelAdmin):
    pass


class ActiviteitAdmin(admin.ModelAdmin):
    pass

class PersoonAdmin(admin.ModelAdmin):
    pass

class ProfileAdmin(admin.ModelAdmin):
    pass

admin.site.register(Locatie, LocatieAdmin)
admin.site.register(Organisatie, OrganisatieAdmin)
admin.site.register(Activiteit, ActiviteitAdmin)
admin.site.register(Persoon, PersoonAdmin)
admin.site.register(Profile, ProfileAdmin)
