## Smoke test 
* Aanmaken twee organisaties, met bijbehorend API token
* Aanmaken locaties voor iedere organisatie
* Aanmaken activiteiten voor iedere organisatie


- [X] Aanmaken superuser

        python manage.py createsuperuser     

- [] Maak alle tagsdefinitions aan

http://localhost:8000/zorg/admin

Zie Readme.md

- [x] Maak user aan per organisatie, in deze test: org1, org2, org3.
      De username moet 4 karakters lang zijn (hetzelfde als de GUID).

    <http://host:port/zorg/admin>
    


- [x] Maak een Profile aan voor elke user met GUID en contactinfo in JSON formaat.
        Kies de GUID hetzelfde als de username.

    <http://localhost:8000/zorg/admin>

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

- [x] Maak een nieuw API token voor elke user

    <http://localhost:8000/zorg/admin>


Token org1: 63d91d2637b48983a7db6b615223e6c24cd6e85f
Token org2: 490e682a1b23490ac899c510d2127a86ce2c9c0a
Token org3: 4342d1b292312109f65a671b47a4161ae58ae555

- [x] Create organisatie


        curl -H "Content-Type: application/json" -H "Authorization: Token 63d91d2637b48983a7db6b615223e6c24cd6e85f" \
        -X POST  \
        -d @post_organisatie1.json \
        http://localhost:8000/zorg/organisatie/

        curl -H "Content-Type: application/json" -H "Authorization: Token 490e682a1b23490ac899c510d2127a86ce2c9c0a" \
        -X POST  \
        -d @post_organisatie2.json \
        http://localhost:8000/zorg/organisatie/

        curl -H "Content-Type: application/json" -H "Authorization: Token 4342d1b292312109f65a671b47a4161ae58ae555" \
        -X POST  \
        -d @post_organisatie3.json \
        http://localhost:8000/zorg/organisatie/
        
- [x] Read organisatie
       
     in elastic


        curl -H "Content-Type: application/json" \
        -X GET  \
        -d @get_search_match_all.json \
        http://localhost:9200/_search   | python -m json.tool
     
     in api
    
        http://localhost:8000/zorg/organisatie/

     with API token (will also display contact field)

         curl -H "Content-Type: application/json" -H "Authorization: Token 63d91d2637b48983a7db6b615223e6c24cd6e85f" \
        -X GET  \
        http://localhost:8000/zorg/organisatie/
        
- [ ] Update organisatie

     curl -H "Content-Type: application/json" -H "Authorization: Token 63d91d2637b48983a7db6b615223e6c24cd6e85f" \
        -X PUT  \
        -d @put_organisatie1.json \
        http://localhost:8000/zorg/organisatie/org1/

- [ ] Delete organisatie

 
- [x]  Create locatie


       curl -H "Content-Type: application/json" -H "Authorization: Token 63d91d2637b48983a7db6b615223e6c24cd6e85f" \
        -X POST  \
        -d @post_locatie_org1_loc1.json \
        http://localhost:8000/zorg/locatie/

       curl -H "Content-Type: application/json" -H "Authorization: Token 63d91d2637b48983a7db6b615223e6c24cd6e85f" \
        -X POST  \
        -d @post_locatie_org1_loc2.json \
        http://localhost:8000/zorg/locatie/

       curl -H "Content-Type: application/json" -H "Authorization: Token 490e682a1b23490ac899c510d2127a86ce2c9c0a" \
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
      
      
     curl -H "Content-Type: application/json" -H "Authorization: Token 63d91d2637b48983a7db6b615223e6c24cd6e85f" \
        -X PUT  \
        -d @put_locatie_org1_loc1.json \
        http://localhost:8000/zorg/locatie/org1-1111/
        
- [ ]  Delete locatie
 
 
       curl -H "Authorization: Token 63d91d2637b48983a7db6b615223e6c24cd6e85f" \
        -X DELETE  http://localhost:8000/zorg/locatie/org1-111/


- [ ] Create persoon

nvt

- [ ] Create activiteit


      curl -H "Content-Type: application/json" -H "Authorization: Token 63d91d2637b48983a7db6b615223e6c24cd6e85f" \
        -X POST  \
        -d @post_activiteit_org1_act1.json \
        http://localhost:8000/zorg/activiteit/

     curl -H "Content-Type: application/json" -H "Authorization: Token  63d91d2637b48983a7db6b615223e6c24cd6e85f" \
        -X POST  \
        -d @post_activiteit_org1_act2.json \
        http://localhost:8000/zorg/activiteit/

     curl -H "Content-Type: application/json" -H "Authorization: Token 63d91d2637b48983a7db6b615223e6c24cd6e85f" \
        -X POST  \
        -d @post_activiteit_org1_act3.json \
        http://localhost:8000/zorg/activiteit/

     curl -H "Content-Type: application/json" -H "Authorization: Token 63d91d2637b48983a7db6b615223e6c24cd6e85f" \
        -X POST  \
        -d @post_activiteit_org1_act4.json \
        http://localhost:8000/zorg/activiteit/

     curl -H "Content-Type: application/json" -H "Authorization: Token 63d91d2637b48983a7db6b615223e6c24cd6e85f" \
        -X POST  \
        -d @post_activiteit_org1_act5.json \
        http://localhost:8000/zorg/activiteit/

     curl -H "Content-Type: application/json" -H "Authorization: Token 490e682a1b23490ac899c510d2127a86ce2c9c0a" \
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


     curl -H "Content-Type: application/json" -H "Authorization: Token 63d91d2637b48983a7db6b615223e6c24cd6e85f" \
        -X PUT  \
        -d @put_activiteit_org1_act1.json \
        http://localhost:8000/zorg/activiteit/org1-11/

- [ ] Delete activiteit


      curl -H "Authorization: Token 63d91d2637b48983a7db6b615223e6c24cd6e85f" \
        -X DELETE  http://localhost:8000/zorg/activiteit/org1-11/



- [ ] Create batch update

        NIET VAN TOEPASSING, nog niet voor productie
      curl -H "Content-Type: application/json" -H "Authorization: Token f5eebed8c8462f9900ead6066de0733c1f54b6e7" \
        -X POST  \
        -d @post_batch.json \
        http://localhost:8000/zorg/_batch_update/
