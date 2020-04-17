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
  
  #### Example query
  The example query will get all artists that are saved in the personal music library.
  `curl -H 'Content-Type: application/json' -H 'Authorization: myapikey'  -X GET "https://oss.anjomro.de/api/v1/artist/" -v
 ---------------------------------------------------------------------------
 
 
### Request Track objects 
Request URL:
https://oss.anjomro.de/api/v1/track/
In the future also: 
https://oss.anjomro.de/api/v1/song/
To avoid triggering keyword based adblockers

 
Curl:
curl -H 'Content-Type: application/json' -H 'Authorization: testapikey'  -X GET "https://oss.anjomro.de/api/v1/track/" -v

 
 
 
 
