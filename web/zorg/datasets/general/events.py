"""
Event handling code

This file contains the functionality needed to handle the event
"""
import logging

from django.contrib.auth.models import User
from django.db import models

from datasets.general.mixins import EventLogMixin
import datasets.normalized as normalized

log = logging.getLogger(__name__)


# For now, using a simple implemetation of concatinating the
# user identifier with the external id, using a dash to
# connect the two. Since we have control over the user identifier
# its possible to guarantee that a dash wont be in it.
def guid_from_id(user_identifier: User, ext_id: str) -> str:
    """
    Generating the systems own guid from the external id
    and the user identifier. The GUID needs to be associated with
    the user and not easily representable. This allows us to know
    which user did what, and prevent users from overwriting each
    others data, while mainting a reversible reference to the own
    user's id
    """
    profile = normalized.models.Profile.objects.get(auth_user=user_identifier)
    return f"{profile.guid}-{ext_id}"


def id_from_guid(user_identifier_len: int, guid: str) -> str:
    """
    Giving a guid, returns the user original id
    """
    return guid[user_identifier_len + 1:]


def handle_event(event: EventLogMixin, model: models.Model) -> bool:
    """
    This is called whenever an event is created
    Based on the data within the event one of 3 actions
    take place in the read optimize table. The actions
    are mapped to the HTTP call type as per REST. For
    consistency, the rest call term is used as the action name
    - POST: create
    - PUT: update
    - DELETE: delete
    In the event log table there is always a new entry
    created.

    Returns true if event is succesfully handled,
    false otherwise
    """
    if event.event_type == 'C':
        return create(event.guid, event.data, model)
    elif event.event_type == 'U':
        return update(event.guid, event.data, model)
    elif event.event_type == 'D':
        return delete(event.guid, model)
    # Unknown command
    log.error(f'Unknown command {event.event_type}')
    return False


def create(guid: str, data: dict, model: models.Model) -> models.Model:
    """
    In a create the event is logged
    and an entry is created in the read
    optimized table
    """
    item = model(guid=guid)
    for (attr, value) in data.items():
        setattr(item, attr, value)
    item.save()
    return item


def update(guid: str, data: dict, model: models.Model) -> models.Model:
    """
    In an update the event is logged
    and the entry in the read optimized
    table is updated with the new value(s)
    """
    item = model.objects.get(pk=guid)
    for (attr, value) in data.items():
        setattr(item, attr, value)
        if attr.endswith('_id'):
            print (f'Foreign key {value} set on {item}: {getattr(item, attr)}')
    item.save()
    return item


def delete(guid: str, model: models.Model) -> bool:
    """
    In a delete event, the event is logged
    and the read optimized table removes the entry
    """
    success = True
    try:
        item = model.objects.get(pk=guid)
        item.delete()
    except Exception as exp:
        log.error(repr(exp))
        success = False

    return success
