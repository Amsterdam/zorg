import logging

from datasets.normalized import models

log = logging.getLogger(__name__)


def process_updates(organisatie, data):
    """
    Process batch updates
    :param data:
    :return:
    """

    action_dispatch = {
        'insert': _batch_insert,
        'patch': _batch_update,
        'delete': batch_delete,
    }
    res = {
        'insert': 0,
        'patch': 0,
        'delete': 0,
    }

    for req in data:
        operation, records = req.items().__iter__().__next__()
        if action_dispatch[operation](organisatie,
                                      records['locatie'],
                                      records['activiteit']):
            res[operation] += 1
    return res


def _batch_insert(organisatie, locatie, activiteit):
    """
    Batch insert, Inserts a locatie/activieit combi

    :param locatie: A dict with `locatie` info or None
    :param activiteit: A dict with `activiteit` info
    :return: True id a change took place
    """
    res = {'locatie': False, 'activiteit': False,}
    if locatie:
        guid = f"{organisatie.guid}-{locatie.get('id')}"
        event = models.LocatieEventLog(event_type='C', guid=guid, data=locatie)
        event.save()
        log.info(f"Created new `locatie` with guid {guid}.")
        res['locatie'] = True

    if activiteit:
        guid = f"{organisatie.guid}-{activiteit.get('id')}"
        event = models.ActiviteitEventLog(event_type='C', guid=guid, data=activiteit)
        event.save()
        log.info(f"Created new `activiteit` with guid {guid}.")
        res['activiteit'] = True
    return res['activiteit'] | res['locatie']


def _batch_update(organisatie, locatie, activiteit):
    """
    Update/patch locatie and/or activiteit

    :param locatie:
    :param activiteit:
    :return:
    """
    res = {'locatie': False, 'activiteit': False,}
    if locatie:
        guid = f"{organisatie.guid}-{locatie.get('id')}"
        event = models.LocatieEventLog(event_type='U', guid=guid, data=locatie)
        event.save()
        log.info(f"Created new `locatie` with guid {guid}.")
        res['locatie'] = True

    if activiteit:
        guid = f"{organisatie.guid}-{activiteit.get('id')}"
        event = models.ActiviteitEventLog(event_type='U', guid=guid, data=activiteit)
        event.save()
        log.info(f"Created new `activiteit` with guid {guid}.")
        res['activiteit'] = True
    return res['activiteit'] | res['locatie']



def batch_delete(organisatie, locatie, activiteit):
    """
    Delete locatie and/or activiteit

    :param locatie:
    :param activiteit:
    :return:
    """
    if locatie:
        loc_deleted = Locatie.objects.filter(pk=locatie).delete()
        if loc_deleted == 0:
            log.info(f"Delete: `locatie` with guid {locatie['guid']} not found. No delete performed")
        else:
            log.info(f"Delete: `locatie` with guid {locatie['guid']} succeeded")

    if activiteit:
        act_deleted = Activiteit.objects.filter(pk=activiteit).delete()
        if act_deleted == 0:
            log.info(f"Delete: `activiteit` with guid {activiteit['guid']} not found. No delete performed")
        else:
            log.info(f"Deelete: `activiteit` with guid {activiteit['guid']} succeeded")

