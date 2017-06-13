## Smoke test 


- [ ] Aanmaken superuser

        python manage.py createsuperuser     


- [ ] Aanmaken profiel voor nieuwe user: kies GUID, contactinfo in JSON formaat.

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
		
- [ ] Aanmaken nieuw API token

    <http://host:port/zorg/admin>
- [ ] Aanmaken organisatie

        curl -H "Content-Type: application/json" -H "Authorization: Token c3f1c1ab3355187f701ccc08d49753fc86de6423" \
        -X POST  \
        -d @post_organisatie.json \
        http://localhost:8000/zorg/organisatie/

    
- [ ] Read organisatie

- [ ] Update organisatie

- [ ] Delete organisatie

        curl -H "Content-Type: application/json" \
        -X GET  \
        -d @get_search_match_all.json \
        http://localhost:9200/_search   | python -m json.tool

- [ ] 
