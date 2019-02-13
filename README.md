# Text Message Service
A RESTFUL API service for sending and retrieving text messages.
This is a very simple service utilizing the "Client url" cURL, \
for sending and retrieving messages. Messages are stored in a sqlite3
database which is included with the python standard library.


## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. \
```git clone git@github.com:ryank01/message-rest-service.git``` 

## Sqlite3 schema
|Field  |Type |Description  |
| :-----| :---:| -----------:|
|  ID     |  int    |     A row identifier, auto-incrementing       |
|  identifier| text |     Unique identifier for recipient e.x email, phone number          |
|  message_body| text |   Message details                             |
|  date_created| int |    Time record was created in database
|  fetched      | int |   Indicate if message was previosuly fetched or not, 1 if it was and 0 if it was not | 

### Prerequisites
Ensure you are running a version of python 3 and you have virtualenv, cURL and Flask installed. These instructions
are geared towards a unix environment.

```
cd ~/sms-app$
~/sms-app$ source env/bin/activate
```
The above will enable the python virtualenv which will allow testing to begin.


## Running the tests
```
~/sms-app$ python3 app.py
```
This will start the flask webserver which will be ready to process client requests.


### Interacting with the service
Open a new terminal window and execute the following commands.

#### Sending a message
The endpoint exposed to send messages is ```http://127.0.0.1:5000/sms-service/api/v1.0/messages```
To send a message use cURL to send a post request to the above url, passing identifier and message_body
as json data. Once this is successful the message is stored in the messages table. \
Example:
  ```
  ~/sms-app$ curl -i -H "Content-Type: application/json" \
   > -X POST -d '{"identifier":"testingservice@email.com","message_body":"hello world"}' \
   > http://127.0.0.1:5000/sms-service/api/v1.0/messages
  ```
  Response: \
    ```
      HTTP/1.0 200 OK
  Content-Type: application/json
  Content-Length: 41
  Server: Werkzeug/0.14.1 Python/3.6.7
  Date: Wed, 13 Feb 2019 05:57:20 GMT
  {
    "msg": "Record successfully added"
  }
    ```
    
#### Retrieving messages
There are three ways of retrieving messages, you can retrieve all messages including the ones previously fetched ordered by time
according to a start and stop index, retrieve messages that were not previosuly fetched meaning if new messages were added
fetch those and lastly fetch a single message based on an id.

##### Retrieve messages according to start, stop index 
Example: \
Notice how the start and stop index were both passed as json data
  ```
  ~/sms-app$ curl -i -H "Content-Type: application/json" -X GET -d '{"start":"1","stop":"4"}' http://127.0.0.1:5000/sms-service/api/v1.0/messages

  ```
Response: \
Pay close attention to the fetched key in the response data (it is either 1 0r 0) 1 indicating the message was previously fetched
and 0 indicating the message was not previously fetched.
  ```
  HTTP/1.0 200 OK
  Content-Type: application/json
  Content-Length: 959
  Server: Werkzeug/0.14.1 Python/3.6.7
  Date: Wed, 13 Feb 2019 06:22:13 GMT
  
  {
    "messages": [
      {
        "ID": 7,
        "date_created": "2019-02-13 05:57:20.216915",
        "fetched": 1,
        "identifier": "jordan@axecapital.com",
        "message_body": "stop all trades"
      },
      {
        "ID": 5,
        "date_created": "2019-02-13 00:30:26.124135",
        "fetched": 0,
        "identifier": "2124563467",
        "message_body": "can we order some food?"
      }
     ]
  }
  ```
  ###### Retrieve messages not previosuly fetched
  Example: \
    ```
    ~sms-app$ curl -X GET http://127.0.0.1:5000/sms-service/api/v1.0/messages 
    ```\
  Response: \
  Again pay close attention to the fetched key in the response (it is set to 0) indicating the message was not previously
  fetched.
  ```
    {
      "messages": [
        {
          "ID": 9,
          "date_created": "2019-02-13 08:17:27.516070",
          "fetched": 0,
          "identifier": "marci@scioncapital.com",
          "message_body": "I need a cds"
        }
      ]
    }
    
  ```
  
  ##### Retrieve a single message
  Example: \
    ```
    ~sms-app$ curl -X GET http://127.0.0.1:5000/sms-service/api/v1.0/messages/<message_id>
    ```
    
   Response: 
     
      {
        "messages": [
          {
            "ID": 5,
            "date_created": "2019-02-13 08:17:27.516070",
            "fetched": 1,
            "identifier": "ryan@scioncaptial.com",
            "message_body": "buying an option"
          }
         ]
      }
      
### Delete a message
Remove a message from the database \
Example: \
```curl -i -X DELETE http://127.0.0.1:5000/sms-service/api/v1.0/messages/<message_id>```

Response: 
```
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 43
Server: Werkzeug/0.14.1 Python/3.6.7
Date: Wed, 13 Feb 2019 04:50:03 GMT

{
  "msg": "Record successfully deleted"
}

```


   
