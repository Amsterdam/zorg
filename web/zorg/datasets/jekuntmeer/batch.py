"""
Bij jekuntmeer is een organisatie een lokatie van een activiteit

from datasets.jekuntmeer import batch
batch.import_data()

from datasets.normalized import models
models.LocatieEventLog.objects.count()
"""
# Python
import json
# Packages
import requests
import xmltodict
# Project
from datasets.normalized import models

USER_GUID = 'jekm'
OFFESET_STEP = 100

URLS = {
    'activiteiten':  'http://amsterdam.jekuntmeer.nl/beheer/eigen-projecten/projects/inforing?c-Offset={offset}',
    'activiteitenDetails': 'http://amsterdam.jekuntmeer.nl/aanbod/eigen-projecten/detail/{activiteit_id}/2/inforing',
    'organisaties': 'http://amsterdam.jekuntmeer.nl/aanbod/eigen-projecten/orglist/inforing',
    'organisatieDetails': 'http://amsterdam.jekuntmeer.nl/aanbod/eigen-projecten/orgdetail/{location_id}/inforing',
}


def normalize_location(data):
    """
    <ORGANISATION> 
   <ID>1367</ID> 
   <NAAM>Humanitas afdeling Amsterdam</NAAM> 
       <ADRES>Sarphatistraat 4</ADRES> 
   <POSTCODE>1017 WS</POSTCODE> 
   <PLAATS>Amsterdam</PLAATS> 
   <TELEFOON>020-7735742</TELEFOON> 
   <EMAIL>kantoor.amsterdan@humanitas.nl</EMAIL> 
   <WEBSITE>www.humanitas.nl/afdeling/amsterdam</WEBSITE> 
       <BACKOFFICES AANTAL="5"> 
              <BACKOFFICE> 
         <ID>1179</ID> 
         <NAAM>Humanitas</NAAM> 
      </BACKOFFICE> 
              <BACKOFFICE> 
         <ID>4726</ID> 
         <NAAM>Humanitas</NAAM> 
      </BACKOFFICE> 
              <BACKOFFICE> 
         <ID>6145</ID> 
         <NAAM>Humanitas Amsterdam en Diemen</NAAM> 
      </BACKOFFICE> 
              <BACKOFFICE> 
         <ID>1743</ID> 
         <NAAM>Sarphatistraat 4</NAAM> 
      </BACKOFFICE> 
              <BACKOFFICE> 
         <ID>1736</ID> 
         <NAAM>spreekuur vrijdag van 10 uur tot 12 uur</NAAM> 
      </BACKOFFICE> 

   </BACKOFFICES> 

    </ORGANISATION>
    """
    # Normalizing postcode to be 6 chars long
    try:
        postcode = data['ORGANISATION'].get('POSTCODE', '').replace(' ', '')
    except AttributeError:
        postcode = None
    return {
        'id': data['ORGANISATION']['ID'],
        'naam': data['ORGANISATION']['NAAM'],
        'openbare_ruimte_naam': data['ORGANISATION']['ADRES'],
        'postcode': postcode,
    }


def load_org():
    try:
        return models.Organisatie.objects.get(pk='jekuntmeer')
    except models.Organisatie.DoesNotExist:
        # Creating the jekuntmeer organistaie. Dit moet uit de poc
        jekuntmeer = models.Organisatie(id='jekuntmeer')
        jekuntmeer.guid = USER_GUID
        jekuntmeer.naam = 'jekuntmeer.nl'
        jekuntmeer.beschrijving = 'Jekuntmeer.nl is de site voor vraag en aanbod in passend werk, opleiding en activiteiten bij jou in de buurt.'
        jekuntmeer.afdeling = ''
        jekuntmeer.contact = {'tel': '085 - 273 36 37', 'email': 'redactie@jekuntmeer.nl'}
        jekuntmeer.save()


def import_data():
    # Loading the organisatie
    org = load_org()

    # Retriving the locations, refered to as organistaie in the xml
    xml_resp = requests.get(URLS['organisaties'])
    locations = xmltodict.parse(xml_resp.text)
    for location in locations['ORGANISATIONS']['ORGANISATION']:
        location_id = location['ID']
        # Creating a location event
        try:
            location_xml = requests.get(URLS['organisatieDetails'].format(location_id=location_id))
            location_data = xmltodict.parse(location_xml.text)
        except Exception as e:
            print(repr(e))
            continue
        guid = f'{USER_GUID}-{location_id}'
        print(guid)
        data = normalize_location(location_data)
        event = models.LocatieEventLog(event_type='C', guid=guid, data=data)
        event.save()

    # Retriving the locations, refered to as organistaie in the xml
    # Making sure at least one request is sent
    offset = 0
    total = 1

    while offset < total:
        xml_resp = requests.get(URLS['activiteiten'].format(offset=offset))
        activiteiten = xmltodict.parse(xml_resp.text)

        for activiteit in activiteiten['PRODUCTEN']['PRODUCT']:
            # Reading the activiteit data
            activiteit_xml = requests.get(URLS['activiteitenDetails'].format(activiteit_id=activiteit['ID']))
            try:
                activiteit_data = xmltodict.parse(activiteit_xml.text)['PRODUCT']
            except Exception as e:
                print(repr(e))
                continue
            guid = f"{USER_GUID}-{activiteit['ID']}"
            print(guid)
            data = {
                'locatie_id': f"{USER_GUID}-{activiteit_data['ORGANISATIEID']}",
                'naam': activiteit_data['NAAM'],
                'beschrijving': activiteit_data['OMSCHRIJVING'],
                'bron_link': URLS['activiteitenDetails'].format(activiteit_id=activiteit_data['ID'])
            }
            event = models.ActiviteitEventLog(event_type='C', guid=guid, data=data)
            event.save()

        # Setting total the first time only
        if total == 1:
            total = int(activiteiten['PRODUCTEN']['@MAXAANTAL'])
        offset += OFFESET_STEP
