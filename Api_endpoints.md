## Api endpoints

De zorg api beschikt over twee soorten endpoints, nl. Data en zoek

### Data endpoints:

- **Organisatie**: https://api.data.amsterdam.nl/zorg/organisatie/
- **Locatie**: https://api.data.amsterdam.nl/zorg/locatie/
- **Activiteit**: https://api.data.amsterdam.nl/zorg/activiteit/

Voor detailspecificaties van velden zie einde van dit document.

### Zoek endpoints:

**Naam/Omschrijving**: https://api.data.amsterdam.nl/zorg/zoek/

De tekstzoek url verwacht een `query` parameter met de querystring.
bijvoorbeeld: `<url>?query=zoektekst`.

**Geolocatie**: https://api.data.amsterdam.nl/zorg/zoek/geo/

De geolocatie heeft lat & lon parameters nodig. Optioneel kan hier ook gebruik gemaakt worden van de `query` parameter.


### Authenticatie

Voor het ophalen van data via een `http GET request` is geen authenticatie nodig. 
Het toevoegen en wijzigen van data vereist een API token.

[Voor meer informatie over API tokens](https://scotch.io/tutorials/the-ins-and-outs-of-token-based-authentication) en 
[hoe deze te implemeteren](http://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication).


#### Nog aan gewerkt zoek eindpunten

- **Organisatie**: https://api.data.amsterdam.nl/zorg/zoek/organisatie/
- **Locatie**: https://api.data.amsterdam.nl/zorg/zoek/locatie/
- **Activiteit**: https://api.data.amsterdam.nl/zorg/zoek/activiteit/

Deze eindpunten zijn nog niet geïmplementeerd. De data dat ze terug geven ziet hetzelfde uit als de tekst zoek url eindpunt

## Data model

De applicatie genereerd zelf een guid op basis van de gebruiker en de id in de call. De guid mag niet gegeven worden in de creatie call (als het erin staat wordt het genegeerd). Voor lezen/ updaten / verwijderen moet de guid gebruikt worden.

Dit is noodzaklijk om meerdere partijen dezelfde id te laten gebruiken terwijl de zorg app ze van elkaar kan scheiden. Op termijn is de bedoeling om ook eigen id te kunnen gebruiken voor lezen / updaten /verwijderen, maar dat is nu buiten scope.

#### Guid
Guid wordt gebruik om een id te koppelen aan data entiteiten die gegarandeerd unique zijn. De guid wordt door het systeem zelf gegenereeed op basis van de gebruiker en de extene partij's eigen id voor die data. Als een guid wordt meegegeven in een post of een put, is die dan genegeerd en wordt door het systeem overgeschregven.

### Organisatie

- id String external id
- guid String, primary key
- naam String
- beschrijving String, optional
- afdeling String, optional
- contact JSON object  for tele, fax, email, www etc.

### Locatie

- id String external id
- guid String, primary_key
- naam String
- openbare_ruimte_naam String, Optional
- postcode String, Optional
- huisnummer String, Optional
- huisletter String, Optional
- huisnummer_toevoeging String, Optional
- bag_link Url, Optional
- geometrie GeoPoint, Optional

Voor de locatie of een geo-punt of een postcode is noodzakelijk. De applicatie probeert op basis van de postcode en evt huisnummer een geo-positie te bepalen en een link naar de bag nummeraanduiding item te leggen.

### Activiteit

- id String external id
- guid String, primary_key
- naam String
- beschrijving String, mag heel lang zijn
- bron_link URL naar de activiteit op de site van de provider
- contactpersoon String
- locatie_id GUID van de locatie
- organisatie_id GUID van de organisatie

Zoeken geef de objecten terug gepakt in een elastic json
