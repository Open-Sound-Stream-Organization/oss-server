# Documentation for OSS Server API 
 
This documentation shows all functions of the OSS Server API.
As a REST-API it with the HTTP methods 'POST', 'GET', 'DELETE' and 'PUT'.

The functions of the API will be clearly explained with corresponding examples.
The respective URL is shown as well as the Curl command 
with all required parameters.

--------------------------------------------------------------------------
Explanation of parameters:

- `-H 'Content-Type: application/json'` specifies, that json as format is used, with a GET-Request this will mean the response from the server will be in json format, with a POST request this means that teh provided data in the request body needs to be in JSON. XML can be also utilzed with changing the mime-type `application/xml`.
- `-H 'Authorization: apikey'` is used to authorize the request; in place of `apikey` the respective API-Key must be used

- `-X HTTP-METHOD "https://example.com/api/v1/resource/" -v` 
HTTP-METHOD can be `GET`, `POST`, `PUT` and `DELETE`.
- `GET`-> Show object(s)
- `POST` -> Create new object
- `PUT` -> Update existing object
- `DELETE` -> Delete an existing object
Explain: Difference of List/Detailview; Detail in the form of https://example.com/api/v1/resource/{id}/
Possible methods: List:GET ; Detail: GET/POST/PUT/DELETE
URL depends on the the resource that needs to be accessed and the server where the api is accessible 

##### Example query

The example query will get all artists that are saved in the personal music library.

	curl -H 'Content-Type: application/json' -H 'Authorization: myapikey'  -X GET "https://oss.anjomro.de/api/v1/artist/" -v
---------------------------------------------------------------------------
 
 
## Request Track objects 

Request URL:
https://oss.anjomro.de/api/v1/song/
	(`song` instead of `track` to avoid triggering keyword based adblockers)

<details>
	<summary>Field Reference</summary>

| identifier | explanation                                 | mandatory                  |
|:----------:|:-------------------------------------------:|:--------------------------:|
| id         | Identifier                                  | is generated automatically |
| title      | name of song                                | yes                        |
| album      | URL to the album the song appears           | yes                        |
| artist     | URL list of the artists that appear         | yes                        |
| mbid       | -                                           | no                         |
| audio      | Audio File, more information in File Upload | no, but sensefull          |
| tags       | Tags                                        | no                         |
</details>
 
<details>
	<summary>Curl-Request-Examples</summary>
GET-Request: Get song 1
	
	curl -H 'Content-Type: application/json' -H 'Authorization: testapikey'  -X GET "https://oss.anjomro.de/api/v1/song/1/" -v

POST-Request: Post new song

 Curl -H 'Content-Type: application/json' -H 'Authorization: testapikey' -X POST -d '{"title":"test5","album":"/api/v1
/album/1/", "artists":[ "/api/v1/artist/2/"]}' "https://oss.anjomro.de/api/v1/song/" -v -H "accept: /"

PUT-Request: Put title of song 1

Curl -H 'Content-Type: application/json' -H 'Authorization: testapikey' -X PUT -d '{"title":"new title"}'  https://oss.anjomro.de/api/v1/song/1/ -v -H "accept: /"

DELETE-Request: Delete song 1

Curl -H 'Authorization: testapikey' -X DELETE  https://oss.anjomro.de/api/v1/song/1/ -v -H "accept: /"
</details>
<details>
	<summary>Sample GET-Response:</summary>

	{
		"meta": {
				"limit": 200,
				"next": null,
				"offset": 0,
				"previous": null,
				"total_count": 1
		},
		"objects": [
				{
						"album": "/api/v1/album/1/",
						"artists": [
								"/api/v1/artist/1/"
						],
						"audio": "repertoire/song_file/1/",
						"id": 1,
						"mbid": "dec720fb-2cdb-4ab6-9217-9aea4ee48566",
						"resource_uri": "/api/v1/song/1/",
						"tags": [
								"/api/v1/tag/1/"
						],
						"title": "Kyrie"
				}
		]
	}
</details>



## Request Album objects 

Request URL:
https://oss.anjomro.de/api/v1/album/

<details>
	<summary>Field Reference</summary>

| identifier | explanation                         | mandatory                  |
|:----------:|:-----------------------------------:|:--------------------------:|
| id         | Identifier                          | is generated automatically |
| name       | name of album                       | yes                        |
| release    | first release of album              | no                         |
| artist     | URL list of the artists that appear | yes                        |
| mbid       | -                                   | no                         |
| cover_url  | URL for cover                       | no                         |
| cover_file | Image of cover                      | no                         |
| tags       | Tags                                | no                         |
</details>
 
<details>
	<summary>Curl-Request-Examples</summary>
GET-Request: Get album 5
	
	curl -H 'Content-Type: application/json' -H 'Authorization: testapikey'  -X GET "https://oss.anjomro.de/api/v1/album/5/" -v

POST-Request: Post new album

 Curl -H 'Content-Type: application/json' -H 'Authorization: testapikey' -X POST -d '{"name":"covertest","cover_url":"
https://de.wikipedia.org/wiki/Bild_am_Sonntag#/media/Datei:Logo_Bild_am_Sonntag_(Bams).svg", "artists":[ "/api/v1/artis
t/2/"]}' "https://oss.anjomro.de/api/v1/album/" -v -H "accept: /"

PUT-Request: Put album 5

		Curl -H 'Content-Type: application/json' -H 'Authorization: testapikey' -X PUT -d '{"name":"covertestnew"}' "https://oss.anjomro.de/api/v1/album/5/" -v -H "accept: /"

DELETE-Request: Delete album 5

		Curl -H 'Authorization: testapikey' -X DELETE  https://oss.anjomro.de/api/v1/album/5/ -v -H "accept: /"
</details>

<details>
	<summary>Sample GET-Response:</summary>

	{
		"meta": {
				"limit": 200,
				"next": null,
				"offset": 0,
				"previous": null,
				"total_count": 1
		},
		"objects": [
				{
				                "name": "A little Jazz Mass",
						"release": null
						"artists": ["/api/v1/artist/1"],
						"cover_url": null,
						"audio": "repertoire/song_file/1/",
						"id": 1,
						"mbid": "dec720fb-2cdb-4ab6-9217-9aea4ee48566",
						"resource_uri": "/api/v1/album/1",
						"songs": ["/api/v1/track/1",
							  "/api/v1/track/2",
							  "/api/v1/track/3",
							  "/api/v1/track/8", 
						 	  "/api/v1/track/9", 
						 	  "/api/v1/track/14", 
						 	  "/api/v1/track/15", 
						 	  "/api/v1/track/23"],
						"tags": [
								"/api/v1/tag/1/"
						],
						
				}
				
				
		]
	}
</details>



## Request Artist objects 

Request URL:
https://oss.anjomro.de/api/v1/artist/

<details>
	<summary>Field Reference</summary>

| identifier 		| explanation                         | mandatory                  |
|:----------:|:-----------------------------------:|:--------------------------:|
| id         	| Identifier                          | is generated automatically |
| name       | name of artist                       | yes                        |
| formation_types    	| Type of Artist (Person/Group/etc.)              | yes                         |
| area     | URL to the area of artist | no                        |
| begin       | Date of persons birth/Date of group formation  | no                         |
| end  | Death/ Group dissolved/ blank if still together | no                         |
| tags       | Tags                                | no                         |
</details>
