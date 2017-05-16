from django.contrib import admin

from .models import Locatie, Organisatie, Activiteit, Persoon, Profile, TagDefinition


class TagDefinitionAdmin(admin.ModelAdmin):
    fields = ('naam', 'category')
    list_display = ('naam', 'category')


class LocatieAdmin(admin.ModelAdmin):
    fields = ('id', 'guid', 'naam', 'openbare_ruimte_naam', 'postcode',
              'huisnummer', 'huisletter', 'huisnummer_toevoeging',
              'bag_link',)
              # 'geometrie')

    list_display = ('id', 'guid', 'naam', 'postcode',
                    'huisnummer', 'huisletter', 'huisnummer_toevoeging')

class OrganisatieAdmin(admin.ModelAdmin):

    fields = ('id', 'guid', 'naam', 'beschrijving', 'afdeling', 'contact', 'locatie')
    list_display = ('guid', 'naam', 'beschrijving', 'afdeling')

class ActiviteitAdmin(admin.ModelAdmin):

    fields = (
        'id', 'guid', 'naam', 'beschrijving', 'bron_link', 'contactpersoon',
        'persoon', 'tags', 'start_time', 'end_time', 'locatie', 'organisatie',
    )
    list_display = ('guid', 'naam', 'locatie', 'organisatie')


class PersoonAdmin(admin.ModelAdmin):
    fields = ('guid', 'naam', 'contact')
    list_display = ('guid', 'naam')


class ProfileAdmin(admin.ModelAdmin):
    pass


admin.site.register(Locatie, LocatieAdmin)
admin.site.register(TagDefinition, TagDefinitionAdmin)
admin.site.register(Organisatie, OrganisatieAdmin)
admin.site.register(Activiteit, ActiviteitAdmin)
admin.site.register(Persoon, PersoonAdmin)
admin.site.register(Profile, ProfileAdmin)
