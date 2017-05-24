from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from datetime import datetime, timedelta

import datasets.normalized as normalized

def create_user():
    """
    Create a user
    """
    auth_user = User.objects.create_user('the_tester', 'test@amsterdam.nl', 'secret')
    auth_user.save()
    user = normalized.models.Profile.objects.create(
        auth_user=auth_user,
        guid='test',
        naam='Jester Tester',
        contact={'tel': '1234'}
    )
    user.save()

    return user

def create_token(user):
    """
    Create a token for a given user
    """
    token = Token.objects.create(user=user)
    token.save()

    return token

def create_organisate(naam='Org', id=1, beschrijving='Dit is een lang verhaal', contact={'tel': '123'}, **kwargs):
    """
    Create a dict that can be passed to the api to create a dict
    """
    org = {
        'naam': naam,
        'id': id,
        'beschrijving': beschrijving,
        'contact': contact
    }
    org.update(kwargs)

    return org

def create_locatie(naam='Loc', id=1, openbare_ruimte_naam='Straat', postcode='1111AA',huisnummer='1', **kwargs):
    loc = {
        'naam': naam,
        'id': id,
        'openbare_ruimte_naam': openbare_ruimte_naam,
        'postcode': postcode,
        'huisnummer': huisnummer
    }
    loc.update(kwargs)

    return loc

def create_activiteit(naam='Activiteit', id=1, beschrijving='Dingen doen', bron_link='http://amsterdam.nl', contactpersoon='Ik', **kwargs):
    act = {
        'naam': naam,
        'id': id,
        'beschrijving': beschrijving,
        'bron_link': bron_link,
        # 'start_time': datetime.now().isoformat(),
        # 'end_time': (datetime.now() + timedelta(14)).isoformat(),
        'contactpersoon': contactpersoon,
        'personen': [],
    }
    act.update(kwargs)

    return act

