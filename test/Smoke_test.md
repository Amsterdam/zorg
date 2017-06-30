## Smoke test 
* Aanmaken twee organisaties, met bijbehorend API token
* Aanmaken locaties voor iedere organisatie
* Aanmaken activiteiten voor iedere organisatie


- [X] Aanmaken superuser

        python manage.py createsuperuser     


- [] Maak alle tagsdefinitions aan

Zie Readme.md

- [x] Maak twee users met bijbehorede profiel voor nieuwe user: kies GUID, contactinfo in JSON formaat.

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
		
- [x] Aanmaken nieuw API tokens

    <http://localhost:8000/zorg/admin>


Token org1: b9a99d7bd94095724da58e895533e6b3a7717d59
Token org2: 1685d1c52861f8cdfd6ae8d2d2e634a30a110538

- [x] Create organisatie


        curl -H "Content-Type: application/json" -H "Authorization: Token b9a99d7bd94095724da58e895533e6b3a7717d59" \
        -X POST  \
        -d @post_organisatie1.json \
        http://localhost:8000/zorg/organisatie/

        curl -H "Content-Type: application/json" -H "Authorization: Token 1685d1c52861f8cdfd6ae8d2d2e634a30a110538" \
        -X POST  \
        -d @post_organisatie2.json \
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

     curl -H "Content-Type: application/json" -H "Authorization: Token b9a99d7bd94095724da58e895533e6b3a7717d59" \
        -X PUT  \
        -d @put_organisatie1.json \
        http://localhost:8000/zorg/organisatie/org1/

- [ ] Delete organisatie

 
- [x]  Create locatie


       curl -H "Content-Type: application/json" -H "Authorization: Token b9a99d7bd94095724da58e895533e6b3a7717d59" \
        -X POST  \
        -d @post_locatie_org1_loc1.json \
        http://localhost:8000/zorg/locatie/

       curl -H "Content-Type: application/json" -H "Authorization: Token b9a99d7bd94095724da58e895533e6b3a7717d59" \
        -X POST  \
        -d @post_locatie_org1_loc2.json \
        http://localhost:8000/zorg/locatie/

       curl -H "Content-Type: application/json" -H "Authorization: Token 1685d1c52861f8cdfd6ae8d2d2e634a30a110538" \
        -X POST  \
        -d @post_locatie_org2_loc1.json \
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
      
      
     curl -H "Content-Type: application/json" -H "Authorization: Token b9a99d7bd94095724da58e895533e6b3a7717d59" \
        -X PUT  \
        -d @put_locatie_org1_loc1.json \
        http://localhost:8000/zorg/locatie/org1-1111/
        
- [ ]  Delete locatie
 
 
       curl -H "Authorization: Token b9a99d7bd94095724da58e895533e6b3a7717d59" \
        -X DELETE  http://localhost:8000/zorg/locatie/org1-111/


- [ ] Create persoon

nvt

- [ ] Create activiteit


      curl -H "Content-Type: application/json" -H "Authorization: Token b9a99d7bd94095724da58e895533e6b3a7717d59" \
        -X POST  \
        -d @post_activiteit_org1_act1.json \
        http://localhost:8000/zorg/activiteit/

     curl -H "Content-Type: application/json" -H "Authorization: Token b9a99d7bd94095724da58e895533e6b3a7717d59" \
        -X POST  \
        -d @post_activiteit_org1_act2.json \
        http://localhost:8000/zorg/activiteit/

     curl -H "Content-Type: application/json" -H "Authorization: Token b9a99d7bd94095724da58e895533e6b3a7717d59" \
        -X POST  \
        -d @post_activiteit_org1_act3.json \
        http://localhost:8000/zorg/activiteit/

     curl -H "Content-Type: application/json" -H "Authorization: Token b9a99d7bd94095724da58e895533e6b3a7717d59" \
        -X POST  \
        -d @post_activiteit_org1_act4.json \
        http://localhost:8000/zorg/activiteit/

     curl -H "Content-Type: application/json" -H "Authorization: Token 1685d1c52861f8cdfd6ae8d2d2e634a30a110538" \
        -X POST  \
        -d @post_activiteit_org2_act1.json \
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


     curl -H "Content-Type: application/json" -H "Authorization: Token b9a99d7bd94095724da58e895533e6b3a7717d59" \
        -X PUT  \
        -d @put_activiteit_org1_act1.json \
        http://localhost:8000/zorg/activiteit/org1-11/

- [ ] Delete activiteit


      curl -H "Authorization: Token f5eebed8c8462f9900ead6066de0733c1f54b6e7" \
        -X DELETE  http://localhost:8000/zorg/activiteit/te01-2288943894839/



- [ ] Create batch update


      curl -H "Content-Type: application/json" -H "Authorization: Token f5eebed8c8462f9900ead6066de0733c1f54b6e7" \
        -X POST  \
        -d @post_batch.json \
        http://localhost:8000/zorg/_batch_update/
