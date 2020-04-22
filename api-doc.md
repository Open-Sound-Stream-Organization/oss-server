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
	
This example query shows a view of all artists. With the URL "https://oss.anjomro.de/api/v1/artist/1/" for example, the data of the first artist can be displayed. Accordingly, the HTTP methods are applied to this URL to modify the entry of the first artist. The following examples demonstrate the handling of a concrete entry like first artist or  third album etc.

But before that it must be clarified how to get an API key:

-------------------------------------------------

## Request API key
As mentioned above, an API key is ALWAYS required for executing commands. To get it, you must first register. Then you have a username and password. Now it is possible to request your API key from OSS. This will now be explained by way of an example:

user:     testuser
password: testuser 

You need a base 64 encoder, for example https://www.base64encode.org/
Encode user:passwort so in this example it is testuser:testuser.

The encoder returns "dGVzdHVzZXI6dGVzdHVzZXI=" in this example.
YOu still have to add a purpose

Now run 
curl -H "Conte	nt-Type: application/json" -H "Authorization: Basic dGVzdHVzZXI6dGVzdHVzZXI=" -X POST -d '{"purpose":"B
ro wser-Session FireFox 20.05"}' "https://oss.anjomro.de/api/v1/apikey" -v

Now you retun your API Key:
{"created": "2020-04-22T13:41:05.659528", "id": 9, "key": "DAy9xQd41dsmxWoXStIYNe2ON2AbVxdTF0PJAvh7ray3GtbZg4J-F-C14aBDv_BLbYOIbd9ACFdYCAb7czhdxoxuds4PILqBCWm-30LCz6x3CbTD9LeVpsXj2SFH2V5Raclt28QYDKU8Z5igtWTVNNAdvL4s4DLj9z2X9HkfgMs", "purpose": "Bro wser-Session FireFox 20.05", "resource_uri": "/api/v1/apikey/9"}* 

The example query now would be
curl -H 'Content-Type: application/json' -H 'Authorization: DAy9xQd41dsmxWoXStIYNe2ON2AbVxdTF0PJAvh7ray3GtbZg4J-F-C14aBDv_BLbYOIbd9ACFdYCAb7czhdxoxuds4PILqBCWm-30LCz6x3CbTD9LeVpsXj2SFH2V5Raclt28QYDKU8Z5igtWTVNNAdvL4s4DLj9z2X9HkfgMs'  -X GET "https://oss.anjomro.de/api/v1/artist/" -v



 
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
	/album/1/", "artists":[ "/api/v1/artist/2/"]}' "https://oss.anjomro.de/api/v1/song/" -v 

PUT-Request: Put title of song 1

	curl -H 'Content-Type: application/json' -H 'Authorization: testapikey' -X PUT -d '{"title":"new title"}' 		 	https://oss.anjomro.de/api/v1/song/1/ -v 

DELETE-Request: Delete song 1

	curl -H 'Authorization: testapikey' -X DELETE  https://oss.anjomro.de/api/v1/song/1/ -v 
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

 	curl -H 'Content-Type: application/json' -H 'Authorization: testapikey' -X POST -d '{"name":"covertest","cover_url":"
	https://de.wikipedia.org/wiki/Bild_am_Sonntag#/media/Datei:Logo_Bild_am_Sonntag_(Bams).svg", "artists":[ "/api/v1/artis
	t/2/"]}' "https://oss.anjomro.de/api/v1/album/" -v 

PUT-Request: Put album 5

		curl -H 'Content-Type: application/json' -H 'Authorization: testapikey' -X PUT -d '{"name":"covertestnew"}' "https://oss.anjomro.de/api/v1/album/5/" -v -H "accept: /

DELETE-Request: Delete album 5

		curl -H 'Authorization: testapikey' -X DELETE  https://oss.anjomro.de/api/v1/album/5/ -v
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
| id         | Identifier                          | is generated automatically |
| mbid         	| musicbrainz_id                          | no |
| name       | name of artist                       | yes                        |
| formation_types    	| Type of Artist (Person/Group/etc.)   max_length=1             | yes                         |
| area     | URL to the area of artist | no                        |
| begin       | Date of persons birth/Date of group formation  | no                         |
| end  | Death/ Group dissolved/ blank if still together | no                         |
| tags       | Tags                                | no                         |

<details>
	<summary>formation_types</summary>

| abbreviation 		| explanation             |
|:----------:|:----------------------------------:|
| P         	| Person 			  |
| G         	| Group 			  |
| O         	| Orchestra 			  |
| C         	| Choir 			  |
| F         	| Character 			  |
| E         	| Other 			  |
</details>

</details>

<details>
	<summary>Curl-Request-Examples</summary>
GET-Request: Get artist 1
	
	curl -H 'Content-Type: application/json' -H 'Authorization: testapikey'  -X GET "https://oss.anjomro.de/api/v1/artist/1/" -v

POST-Request: Post new artist

 	curl -H 'Content-Type: application/json' -H 'Authorization: testapikey' -X POST -d '{"name":"DieExmatrikulatoren","formation_types":"G","begin":"2020-04-20"}' "https://oss.anjomro.de/api/v1/artist/" -v

PUT-Request: Put name of artist 3

	curl -H 'Content-Type: application/json' -H 'Authorization: testapikey' -X PUT -d '{"name":"DieExmatrikulatoren2"}'  https://oss.anjomro.de/api/v1/artist/3/ -v

DELETE-Request: Delete artist 2

	curl -H 'Authorization: testapikey' -X DELETE  https://oss.anjomro.de/api/v1/artist/2/ -v 
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
					"albums": [], 
					"area": "/api/v1/area/1", 
					"begin": null, 
					"end": null, 
					"formation_types": "Group", 
					"id": 506, "mbid": "", 
					"name": "DieBiebos", 
					"resource_uri": "/api/v1/artist/506", 
					"songs": [	  "/api/v1/track/1",
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
					"type": ""
				
				}
				
				
		]
	}
</details>


## Request Area objects 

Request URL:
https://oss.anjomro.de/api/v1/area/

<details>
	<summary>Field Reference</summary>

| identifier 		| explanation                         | mandatory                  |
|:----------:|:-----------------------------------:|:--------------------------:|
| id         | Identifier                          | is generated automatically |
| mbid         	| musicbrainz_id                          | no |
| name       | name of area                       | yes                        |
| area_categories    	| Area type (Country/City/etc.)   max_length=1             | yes                         |
| country_code     | iso-3166-1-code (DE/GB/FR etc.) | no                        |


<details>
	<summary>area_categories</summary>

| abbreviation 		| explanation             |
|:----------:|:----------------------------------:|
| X         	| Country 			  |
| L         	| Subdivision 			  |
| C         	| County 			  |
| M         	| Municipality 			  |
| S         	| City 			  |
| D         	| District 			  |
| I         	| Island 			  |
</details>

</details>

<details>
	<summary>Curl-Request-Examples</summary>
GET-Request: Get area 2
	
	curl -H 'Content-Type: application/json' -H 'Authorization: testapikey'  -X GET "https://oss.anjomro.de/api/v1/area/2/" -v

POST-Request: Post new area

 	curl -H 'Content-Type: application/json' -H 'Authorization: testapikey' -X POST -d '{"name":"Mkg","area_categories":"X"}' "https://oss.anjomro.de/api/v1/area/" -v

PUT-Request: Put name of area 3

	curl -H 'Content-Type: application/json' -H 'Authorization: testapikey' -X PUT -d '{"name":"Schwieberdingen"}'  https://oss.anjomro.de/api/v1/area/3/ -v

DELETE-Request: Delete area

	curl -H 'Authorization: testapikey' -X DELETE  https://oss.anjomro.de/api/v1/area/4/ -v 
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
					"area_categories": "X", 
					"artists": ["/api/v1/artist/1"],
					"country_code": null, 
					"id": 6, 
					"mbid": "", 
					"name": "Muenchen", 
					"resource_uri": "/api/v1/area/6", 
					"type": ""
				
				}
								
		]
	}
</details>


## Request Playlist objects 

Request URL:
https://oss.anjomro.de/api/v1/playlist/

<details>
	<summary>Field Reference</summary>

| identifier 		| explanation                         | mandatory                  |
|:----------:|:-----------------------------------:|:--------------------------:|
| id         | Identifier                          | is generated automatically |
| name       | name of playlist                       | yes                        |
| songsinplaylist     	| tracks in playlist           | no                         |
| tags     | tags in playlist  (Jazz etc.)| no                        |


<details>
	<summary>songsinplaylist</summary>

| identifier 		| explanation                         | mandatory                  |
|:----------:|:-----------------------------------:|:--------------------------:|
| id         | Identifier                          | is generated automatically |
| playlist       | name of playlist                       | no                        |
| song     	| track in playlist           | yes                         |
| sort_number     | opportunity to sort| yes                        |


</details>
</details>

<details>
	<summary>Curl-Request-Examples</summary>
GET-Request: Get playlist 1
	
	curl -H 'Content-Type: application/json' -H 'Authorization: testapikey'  -X GET "https://oss.anjomro.de/api/v1/playlist/1/" -v

POST-Request: Post new playlist

 	curl -H 'Content-Type: application/json' -H 'Authorization: testapikey' -X POST -d '{"name":"Bestoff"}' "https://oss.anjomro.de/api/v1/playlist/" -v

PUT-Request: Put name of playlist 4

	curl -H 'Content-Type: application/json' -H 'Authorization: testapikey' -X PUT -d '{"name":"Thebestsongsever"}'  https://oss.anjomro.de/api/v1/playlist/4/ -v

DELETE-Request: Delete playlist 3

	curl -H 'Authorization: testapikey' -X DELETE  https://oss.anjomro.de/api/v1/playlist/3/ -v 
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
				"id": 5, 
				"name": "GuteLauneRemix", 
				"resource_uri": "/api/v1/playlist/5", 
				"songsinplaylist": 
					[
					{
						"id": 4, 
						"playlist": "/api/v1/playlist/5",
						"resource_uri": "/api/v1/songinplaylist/4", 
						"song": {
							"album": "/api/v1/album/1", 
							"artists": ["/api/v1/artist/4"], 
							"audio": "repertoire/song_file/3/", 
							"id": 3, 
							"mbid": null, 
							"playlists": ["/api/v1/playlist/5"], 
							"resource_uri": "/api/v1/song/3", 
							"tags": [], 
							"title": "TheTrackTitle"}, 
						"sort_number": 1
					}, 
					{
						"id": 5, 
						"playlist": "/api/v1/playlist/5", 
						"resource_uri": "/api/v1/songinplaylist/5", 
						"song": {
							"album": "/api/v1/album/517", 
							"artists": ["/api/v1/artist/557", 
							"/api/v1/artist/566"], 
							"audio": "repertoire/song_file/93/", 
							"id": 93, 
							"mbid": null, 
							"playlists": ["/api/v1/playlist/5"], 
							"resource_uri": "/api/v1/song/93", 
							"tags": [], 
							"title": "The Souls's Children"}, 
						"sort_number": 634
					}
				], 
				"tags": [
					{
						"albums": [], 
						"artists": [], 
						"id": 6, 
						"name": 
						"Rock", 
						"playlists": ["/api/v1/playlist/5"], 
						"resource_uri": "/api/v1/tag/6", 
						"songs": []
					}, 
					{
						"albums": [], 
						"artists": [], 
						"id": 7, 
						"name": "Pop", 
						"playlists": ["/api/v1/playlist/5"], 
						"resource_uri": "/api/v1/tag/7", 
						"songs": []
					}
					]
				}
								
		]
	}
</details>


## Request Tag objects 

Request URL:
https://oss.anjomro.de/api/v1/playlist/

<details>
	<summary>Field Reference</summary>

| identifier 		| explanation                         | mandatory                  |
|:----------:|:-----------------------------------:|:--------------------------:|
| id         | Identifier                          | is generated automatically |
| name       | name of tag (Jazz etc.)             | yes                        |

</details>

<details>
	<summary>Curl-Request-Examples</summary>
GET-Request: Get tag 5
	
	curl -H 'Content-Type: application/json' -H 'Authorization: testapikey'  -X GET "https://oss.anjomro.de/api/v1/tag/5/" -v

POST-Request: Post new playlist

 	curl -H 'Content-Type: application/json' -H 'Authorization: testapikey' -X POST -d '{"name":"Rock"}' "https://oss.anjomro.de/api/v1/tag/" -v

PUT-Request: Put name of playlist 4

	curl -H 'Content-Type: application/json' -H 'Authorization: testapikey' -X PUT -d '{"name":"Jazz"}'  https://oss.anjomro.de/api/v1/tag/5/ -v

DELETE-Request: Delete tag 3

	curl -H 'Authorization: testapikey' -X DELETE  https://oss.anjomro.de/api/v1/tag/3/ -v 
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
					"albums": [], 
					"artists": [], 
					"id": 7, 
					"name": "Pop", 
					"playlists": [], 
					"resource_uri": "/api/v1/tag/7", 
					"songs": []
				}
								
		]
	}
</details>
