import logging

from datasets.normalized.models import Locatie, Activiteit

log = logging.getLogger(__name__)


def process_updates(data):
    """
    Process batch updates
    :param data:
    :return:
    """

    action_dispatch = {
        'insert': batch_insert,
        'patch': batch_update,
        'delete': batch_delete,
    }
    res = {
        'insert': 0,
        'patch:': 0,
        'delete': 0,
    }

    for req in data:
        operation = req['actie']
        if action_dispatch[operation](req['locatie'], req['activiteit']):
            res[operation] += 1
    return res


def batch_insert(locatie, activiteit):
    """
    Batch insert, Inserts a locatie/activieit combi

    :param locatie: A dict with `locatie` info or None
    :param activiteit: A dict with `activiteit` info
    :return: True id a change took place
    """
    if locatie:
        loc, loc_created = Locatie.objects.update_or_create(
            id=locatie.get('id', ''),
            naam=locatie.get('naam', ''),
            openbare_ruimte_naam=locatie.get('openbare_ruimte_naam', ''),
            postcode=locatie.get('postcode', ''),
            huisnummer=locatie.get('huisnummer', ''),
            huisletter=locatie.get('huisletter', ''),
            huisnummer_toevoeging=locatie.get('huisnummer_toevoeging', ''),
        )
        if loc_created:
            log.info(f"Created new `locatie` with guid {loc.guid}.")
        else:
            log.info(f"Tried creating new `locatie` but a `location`"
                     f" with guid {loc.guid} already exists, updated it instead.")
    else:
        log.info(f"No `locatie` info provided.")

    if activiteit:
        act, act_created = Activiteit.objects.update_or_create(
            id=activiteit.get('id', ''),
            naam=activiteit.get('naam', ''),
            beschrijving=activiteit.get('beschrijving', ''),
            afdeling=activiteit.get('afdeling', ''),
            contact=activiteit.get('contact', ''),
            locatie_id=activiteit.get('locatie_id', ''),
        )
        if act_created:
            log.info(f"Created `activiteit` with guid {act.guid}.")
        else:
            log.info(f"Tried creating new `activiteit` but a `activiteit` "
                     f"with guid {loc.guid} already exists, updated it instead.")
    else:
        log.info(f"No `activiteit` info provided.")


def batch_update(locatie, activiteit):
    """
    Update/patch locatie and/or activiteit

    :param locatie:
    :param activiteit:
    :return:
    """
    if locatie:
        loc_updated = Locatie.objects.filter(pk=locatie['guid']).update(**locatie)
        if loc_updated == 0:
            log.info(f"Update: `locatie` with guid {locatie['guid']} not found. Update failed")
        else:
            log.info(f"Update: `locatie` with guid {locatie['guid']} succeeded")
    else:
        log.info(f"Update no `locatie` info provided.")

    if activiteit:
        act_updated = Activiteit.objects.filter(pk=activiteit['guid']).update(**locatie)
        if act_updated == 0:
            log.info(f"Update: `activiteit` with guid {activiteit['guid']} not found. Update failed")
        else:
            log.info(f"Update: `activiteit` with guid {activiteit['guid']} succeeded")
    else:
        log.info(f"Update no `activiteit` info provided.")


def batch_delete(locatie, activiteit):
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

