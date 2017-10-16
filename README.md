## Zorg API
POC voor een zorg API applicatie.

Zie Api_endpoint.md voor api details

### Local dockers and local server
    # start the local docker containers
	docker-compose up -d --build
	
	# create virtual environment (use the appropiate python binary)
	virtualenv -p /usr/local/bin/python3 ~/venv/zorg
    source ~/venv/zorg/bin/activate
    
    # install the requirements in the virtual env
    pip install -r web/requirements.txt

   
    # run database migrations
    cd web/zorg
    python manage.py migrate


    # create elastic index based on document definitions
    cd web/zorg
    python manage.py elastic --build

    # start server
    python manage.py runserver  
   
   	# check out status using
    http://127.0.0.1:8000/zorg/status/health


### Gebruiker en API Token maken
Voor het ophalen van data via een `http GET request` is geen authenticatie nodig.
Het toevoegen en wijzigen van data vereist echter een API token.

1. Maak superuser: `$ python manage.py createsuperuser`
2. Log in: <http://localhost:8000/zorg/admin> 
3. Maak een nieuwe gebruiker aan. Users-add.
4. maak een een token aan voor de nieuwe gebruiker. Tokens-add.
5. maak een nieuwe profiel aan voor de nieuwe gebruiker. Profiles-add
    * Guid = unieke guid voor de organisatie (4 karakters)
    * Naam = naam voor de organisatie
    * Contact = {"email":"email@host"}
5. token meesturen in de `Authorization: Token [value]` header van je requests


[Meer informatie over API tokens](https://scotch.io/tutorials/the-ins-and-outs-of-token-based-authentication)

[Hoe deze te implementeren](http://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication).

####

### Reindex ###
The elastic index can be recreated using the commands.
In acceptance/production environment this command can also be run inside the docker container.

        # Create a copy of the ES index to index '/zorg_backup'
        manage.py --backup_index

        # Delete, build and reindex
        manage.py --delete

        manage.py --build

        manage.py --reindex

        Check resultaat , b.v. via
        http://HOST:8000/zorg/typeahead/?query=y
        of http://HOST:8000/zorg/zoek/?query=yoga

        1) Indien check niet ok--> manage.py --restore_index

        2) indien check ok -->manage.py --delete_backup_index
            
#### Tags #####
   Login on <http://localhost:8000/zorg/admin> and add the required TagDefinitions.

category: "DAG"
naam: "maandag", "dinsdag", "woensdag", "donderdag", "vrijdag", "zaterdag", "zondag"

category: "TIJD"
naam: "ochtend", "middag", "avond", "nacht"

category: "BETAALD"
naam: "gratis", "betaald"

category: "LEEFTIJDSCATEGORIE"
naam: "volwassene", "senior", "jeugd"


The **naam** of these tags can be used in the create activiteit API.


### Test info ####

Zie test/Smoke_test.MD voor voorbeeld requests.


#### Inladen jekuntmeer
Na reguliere deployment van de Zorg docker via jenkins, zijn de volgende manuele stappen nodig:

- login on productie/acceptatie Zorg docker

./manage.py runimport jekuntmeer

./manage.py elastic --backup_index

./manage.py elastic --delete

./manage.py elastic --build

./manage.py elastic --reindex

### Alle activiteiten en locaties verwijderen, maar gebruikers intact laten

Run bash in de docker:
```
docker exec -ti --user root zorg bash
```

Dump alle data:
```
python manage.py dumpdata --indent 2 'auth' > auth.json
python manage.py dumpdata --indent 2 'normalized.organisatie' > organisatie.json
python manage.py dumpdata --indent 2 'normalized.tagdefinition' > tags.json
python manage.py dumpdata --indent 2 'normalized.profile' > profile.json
python manage.py dumpdata --indent 2 'authtoken' > token.json
```

Verwijder alle data:
```
python manage.py flush
python manage.py elastic --delete
python manage.py elastic --build
```

Importeer de users etc in de database:
```
python manage.py loaddata auth.json
python manage.py loaddata organisatie.json
python manage.py loaddata tags.json
python manage.py loaddata profile.json
python manage.py loaddata token.json
```

Re-indexeer de database:
```
python manage.py elastic --reindex
```

### Alles van een bepaalde organisatie verwijderen - Postgres
delete from normalized_activiteit_tags where activiteit_id like 'organisatie%’;
delete from normalized_activiteit where organisatie_id like 'organisatie%’;
delete from normalized_activiteiteventlog where guid like 'organisatie%’;

delete from normalized_locatie where guid like 'organisatie%’;
delete from normalized_locatieeventlog where guid like 'organisatie%';

### Alles van een bepaalde organisatie verwijderen - ElasticSearch
Aangezien alles in dezelfde index wordt opgeslagen, moet documenten op basis van de "_id" (GUID) verwijderd worden:

curl -sS -XPOST '192.168.1.1:9200/zorg_backup/activiteit/_delete_by_query' -H 'Content-Type: application/json' -d'
{
  "query": {
    "wildcard": {
      "_id": "organisatie-*"
    }
  }
}
'
