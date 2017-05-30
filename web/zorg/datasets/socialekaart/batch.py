# Python
import csv

import os

# Project
from datasets.normalized import models

USER_GUID = 'sclk'


def normalize_location(data, location_id):
    # Normalizing postcode to be 6 chars long
    try:
        postcode = data.get('postcode', '').replace(' ', '')
    except AttributeError:
        postcode = None

    return {
        'id': location_id,
        'naam': data['kaart'],
        'openbare_ruimte_naam': data['straat'],
        'postcode': postcode,
        'huisnummer': data['huisnummer'],
        'huisnummerletter': data['huisnummerletter'],
        'huisnummer_toevoeging': data['huisnummertoevoeging']
    }


def normalize_activity(data, location_guid, activity_id):
    return {
        'id': activity_id,
        'locatie_id': location_guid,
        'organisatie_id': f'{USER_GUID}',
        'naam': data['kaart'],
        'beschrijving': data['bijzonderheden'],
        'bron_link': data['www'],
    }


def load_org():
    try:
        return models.Organisatie.objects.get(pk='socialekaart')
    except models.Organisatie.DoesNotExist:
        # Creating the socialekaart organistaie. Dit moet uit de poc
        socialekaart = models.Organisatie(id='socialekaart')
        socialekaart.guid = USER_GUID
        socialekaart.naam = 'socialekaart.amsterdam.nl'
        socialekaart.beschrijving = 'Socialekaart is de site voor vraag en aanbod in passend werk, opleiding en activiteiten bij jou in de buurt.'
        socialekaart.afdeling = ''
        socialekaart.contact = {'email': 'socialekaart@ggd.amsterdam.nl'}
        socialekaart.save()


def import_location(row):
    # Location creation event from the dict
    # Since there is no reference to an id, using postcode and house number as id
    location_id = f"{row['postcode']}{row['huisnummer']}"
    guid = f'{USER_GUID}-{location_id}'
    data = normalize_location(row, location_id)
    event = models.LocatieEventLog(event_type='C', guid=guid, data=data)
    event.save()
    return guid


def import_activity(row, location_guid):
    # Location creation event from the dict
    # Since there is no reference to an id, using postcode and house number as id
    activity_id = f"{row['postcode']}{row['huisnummer']}"
    guid = f'{USER_GUID}-{activity_id}'
    data = normalize_activity(row, location_guid, activity_id)
    event = models.ActiviteitEventLog(event_type='C', guid=guid, data=data)
    event.save()


def load_csv(path=None):
    csv_data = None
    # If no path is given switching to default
    if not path:
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data/ska_export.csv')
        with open(path, encoding='latin-1') as csv_file:
            csv_data = csv.DictReader(csv_file, delimiter=';')
            for row in csv_data:
                location_guid = import_location(row)
                import_activity(row, location_guid)
        return csv_data


def run():
    # Loading the organisatie
    load_org()
    # Retrieving from the csv
    csv_data = load_csv()
