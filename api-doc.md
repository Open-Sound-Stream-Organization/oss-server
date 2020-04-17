
 Documentation for OSS Server API 
 
 This documentation shows all functions of the OSS Server API.
 As a REST-API it with the HTTP methods 'POST', 'GET', 'DELETE' and 'PUT'.
 
 The functions of the API will be clearly explained with corresponding examples.
 The respective URL is shown as well as the Curl command 
 with all required parameters.
 
 --------------------------------------------------------------------------
 **Make sure to install the docker <br> (https://github.com/Open-Sound-Stream-Organization/oss-server/blob/master/README.md) to run the commands** <br> <br>
 Explanation of parameters:
 
 **-H 'Content-Type: application/json'** <br>
 is the format of the output; could also be 
 -H 'Content-Type: application/xml'
 
 **-H 'Authorization: testapikey'** <br>
 testapikey must be the respective API-Key
  
 **-X HTTP-METHOD "URL" -v** <br>
  HTTP-METHOD can be 'POST', 'GET', 'DELETE' and 'PUT'.
  URL depends on the the wanted functionality to implement 
 
 ---------------------------------------------------------------------------
 
 File Download:
 
 Request URL:
 https://de0.win/api/v1/track/
 
 Curl:
 Curl -H 'Content-Type: application/json' -H 'Authorization: testapikey'  -X GET "https://de0.win/api/v1/track/" -v
 
 
 
 
