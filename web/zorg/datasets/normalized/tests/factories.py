from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

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

def create_organisate(naam='Org', id=1, beschrijving='Dit is een lang verhaal', contact={'tel': '123'}, guid=None):
    """
    Create a dict that can be passed to the api to create a dict
    """
    org = {
        'naam': naam,
        'id': id,
        'beschrijving': beschrijving,
        'contact': contact
    }
    if guid:
        org['guid'] = guid

    return org
