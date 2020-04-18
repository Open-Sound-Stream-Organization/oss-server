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
 
 
### Request Track objects 

Request URL:
https://oss.anjomro.de/api/v1/song/
	(`song` instead of `track` to avoid triggering keyword based adblockers)

 
<details>
	<summary>Curl-Request-Examples</summary>
GET-Request:
	
	curl -H 'Content-Type: application/json' -H 'Authorization: testapikey'  -X GET "https://oss.anjomro.de/api/v1/song/" -v

POST-Request:

 Curl -H 'Content-Type: application/json' -H 'Authorization: testapikey' -X POST -d '{"title":"test5","album":"/api/v1
/album/1/", "artists":[ "/api/v1/artist/2/"]}' "https://oss.anjomro.de/api/v1/track/" -v -H "accept: /"

PUT-Request:

		TODO: curl-example-put-request

DELETE-Request:

		TODO: curl-example-delete-request
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
<details>
	<summary>Field Reference</summary>

|  identifier  |              Explanation              | required when creating a new object |
|:------------:|:-------------------------------------:|:-----------------------------------:|
|      id      |                  ...                  |     no, generated automatically     |
|     title    |             name of track             |                 yes                 |
|     album    | Link to the album the song appears in |                 yes                 |
|    artists   |                                       |                                     |
|     mbid     |             Musicbrainz ID            |                  no                 |
|     audio    |                                       |                                     |
|     tags     |                                       |                                     |
| resource_uri |                                       |                                     |

</details>
