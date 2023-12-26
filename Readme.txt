Messaging System API
A simple REST API backend system designed to handle messages between users. This system allows users to send, receive, read, and delete messages. It's built to be clean, simple, and production-ready.

Features
Send Messages: Users can send messages with a subject and content.
Retrieve Messages: Users can retrieve all their messages or only the unread ones.
Read a Message: Access the content of a specific message.
Delete Messages: Users can delete messages they own or have received.

User Authentication: Implement user authentication to ensure users read/get/delete only their messages.
Database Integration: all user and message data stored in a database.
Technology Stack
Backend Framework: Django
Database: Sqlite3.
Getting Started
Prerequisites

Installation
Clone the repository to your local machine.
Navigate to the project directory and install:

Step 1:
python -m venv venv

Step 2:
Activate the virtual environment:

- On Linux and macOS:
source venv/bin/activate

- On Windows:
venv\Scripts\activate


Step 3:
pip install -r requirements.txt

Step 4:
create .env file inside the root folder of the project, with the following keys:
LOGGER_LEVEL {can be INFO, DEBUG, WARNING etc)
DJANGO_SECRET_KEY {django secret key)

Step 5:
python manage.py makemigrations

Step 6:
python manage.py migrate

Step 7:
- Then you can run the application:
manage.py runserver


API Endpoints:

I wrote a python file called 'test_requests.py' inside the root folder.
There you can find there all the functions that you need for testing and interact with the API.
Here you can find an extended explanation about each function.


Because Django works with CSRF token,
and we want to interact with Django just with jsons and not using UI at all,
We should get the CSRF Token, and store it both in the cookies and in the headers.
We can use the funtion 'get_csrf_token()' for setting the CSRF token.
{
    path: GET /users/token
    json: None
}


For starting the interaction with the messages system we need to registry a user.
We can use the funtion 'register(username, email, password)' and submit 3 arguments
{
    path: POST /users/register
    json: {
       "username": username,
       "email": email,
       "password": password,
    }
}

After we registered the user, we should log in with his details
We can use the funtion 'login(username, password)' and submit 2 arguments
{
    path: POST /users/login
    json: {
       "username": username,
       "password": password,
    }
}

At the end of the interaction we should log out from this user
We can use the funtion 'logout()'
{
    path: POST /users/logout
    json: None
}

For getting all the messages ids' received by the user,
We can use the funtion 'get_messages_id()'
{
    path: GET /messages/messages_per_receiver
    json: None
}
the function returns a json with a list of messages ids':
{
    'messages_id',[<message_id>, <message_id>, <message_id>]
}

For getting all the messages ids' received by the user and classified as unread,
We can use the funtion 'get_unread_messages_id()'
{
    path: GET /messages/unread_per_receiver
    json: None
}
the function returns a json with a list of messages ids':
{
    'messages_id',[<message_id>, <message_id>, <message_id>]
}

For read a message received by the user,
We can use the funtion 'read_message(message_id)' and submit 1 argument
{
    path: GET /messages/read_message
    json: {
        "message_id": message_id
    }
}
the function returns a json with the arguments:
{
    'sender_id', 'receiver_id', 'subject', 'body', 'creation_date'
}

For delete a message received or sent by the user,
We can use the funtion 'delete_message(message_id)' and submit 1 argument
{
    path: DELETE /messages/delete_message
    json: {
        "message_id": message_id
    }
}

