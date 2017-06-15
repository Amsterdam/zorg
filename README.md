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


### API Token maken
1. `$ python manage.py createsuperuser` en stappen volgen
2. in je browser naar http://localhost:8000/zorg/admin en inloggen
3. onder “Tokens” een token maken voor je superuser (of maak eerst een andere user aan)
4. onder “Profiles” een paar gegevens invullen voor je user
5. token meesturen in de `Authorization: Token [value]` header van je requests

#### 

### Reindex ###
The elastic index can be recreated using the commands.
In acceptance/production environment this command can also be run inside the docker container.

           python manage.py elastic --delete
           python manage.py elastic --build
           python manage.py elastic --reindex
            
#### Tags #####
   Login on <http://localhost:8000/zorg/admin> and add the required TagDefinitions.

category: "DAG"
naam: "maandag", "dinsdag", "woensdag", "donderdag", "vrijdag", "zaterdag", "zondag"

category: "TIJD"
naam: "ochtend", "middag", "avond", "nacht"

category: "BETAALD"
naam: "gratis", "betaald"

The **naam** of these tags can be used in the create activiteit API.