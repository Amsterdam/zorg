## Smoke test 


- [X] Aanmaken superuser

        python manage.py createsuperuser     


- [x] Aanmaken profiel voor nieuwe user: kies GUID, contactinfo in JSON formaat.

    <http://host:port/zorg/admin>
    
    
        { "contact":
            {   "telefoon": {
                    "tel1": "01234567890",
                    "tel2": "01234567890"
                },
                "website":{
                    "home": "http://nu.nl"
                }
    
            }
         }
		
- [x] Aanmaken nieuw API token

    <http://host:port/zorg/admin>
- [x] Create organisatie


        curl -H "Content-Type: application/json" -H "Authorization: Token 4dc46119f481443621efbe15035957ae9a07f4d9" \
        -X POST  \
        -d @post_organisatie.json \
        http://localhost:8000/zorg/organisatie/

   
        
- [x] Read organisatie
       
     in elastic


        curl -H "Content-Type: application/json" \
        -X GET  \
        -d @get_search_match_all.json \
        http://localhost:9200/_search   | python -m json.tool
     
     in api
    
        http://localhost:8000/zorg/organisatie/
        
- [ ] Update organisatie

- [ ] Delete organisatie

 
- [x]  Create locatie


       curl -H "Content-Type: application/json" -H "Authorization: Token 4dc46119f481443621efbe15035957ae9a07f4d9" \
        -X POST  \
        -d @post_locatie.json \
        http://localhost:8000/zorg/locatie/

- [x]  Read locatie
in elastic


        curl -H "Content-Type: application/json" \
        -X GET  \
        -d @get_search_locatie.json \
        http://localhost:9200/_search   | python -m json.tool
     
in api

        http://localhost:8000/zorg/locatie/
- [ ]  Update locatie
      
      
     curl -H "Content-Type: application/json" -H "Authorization: Token 4dc46119f481443621efbe15035957ae9a07f4d9" \
        -X PUT  \
        -d @put_locatie.json \
        http://localhost:8000/zorg/locatie/1235-7843278492/
        
- [ ]  Delete locatie
 
 
       curl -H "Authorization: Token 4dc46119f481443621efbe15035957ae9a07f4d9" \
        -X DELETE  http://localhost:8000/zorg/locatie/te01-7843278492/


- [ ] Create persoon


      curl -H "Content-Type: application/json" -H "Authorization: Token 4dc46119f481443621efbe15035957ae9a07f4d9" \
        -X POST  \
        -d @post_persoon.json \
        http://localhost:8000/zorg/persoon

- [ ] Create activiteit


      curl -H "Content-Type: application/json" -H "Authorization: Token 4dc46119f481443621efbe15035957ae9a07f4d9" \
        -X POST  \
        -d @post_activiteit.json \
        http://localhost:8000/zorg/activiteit/

- [ ] Read activiteit
in elastic


        curl -H "Content-Type: application/json" \
        -X GET  \
        -d @get_search_activiteit.json \
        http://localhost:9200/_search   | python -m json.tool
     
in api
    
        http://localhost:8000/zorg/activiteit/
- [ ] Update activiteit


     curl -H "Content-Type: application/json" -H "Authorization: Token 4dc46119f481443621efbe15035957ae9a07f4d9" \
        -X PUT  \
        -d @put_activiteit.json \
        http://localhost:8000/zorg/activiteit/1235-9888943894839/

- [ ] Delete activiteit


      curl -H "Authorization: Token 4dc46119f481443621efbe15035957ae9a07f4d9" \
        -X DELETE  http://localhost:8000/zorg/activiteit/te01-9888943894839/

