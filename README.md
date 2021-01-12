# CS50 Final Project 
## About the project
Instado is an social network app where:
  - Users can post pictures 
  - Users can add friend to each other 
  - User who became friends can chat with each other

## Tools
  - Frontend: HTML, CSS, Bootstrap, JavaScript
  - Backend: Django
  - Frontend to backend communication: JQuery

### Tech
In this project we take advantage of some frameworks, open source projects to make things work properly:
* Django REST framwork - for building Web APIs
* Channels - for using WebSocket protocol to create real-time chat application

### Structure
* **accounts**
    * **models.py**: create User, Profile, FriendRequest models
    * **forms.py**: contains UserRegisterForm and ProfileUpdateForm
    * **serializers.py**: create UserSerializer and FriendListSerializer
    *  **api.py**: write API views which ultizes UserSerializer and FriendListSerializer
    *  **urls.py**: configuration of the app's URLs 
    *  **views.py**: functions to handle register, display of a user's profile, profile editing, display of friendlist, display of suggested users to add friends, sending/canceling friend request and unfriend action.
    *  **templates/accounts**
        * **layout.html** 
        * **register.html**
        * **login.html**
        * **logout.html**
        * **profile.html**
        * **edit_profile.html**
        * **users_list.html**
        * **friend_list.html**
    * **static/accounts**
        * **styles.css**
        * **profile_action.js**: handle what will happen after a user clicks Add Friend button
* **chat**
    * **models.py**: create Message model
    * **serializers.py**: create MessageSerializer
    *  **api.py**: write API views which ultizes MessageSerializer
    *  **urls.py**
    *  **views.py**
    *  **routing.py**: routing configuration to lookup a consumer handler
    *  **consumers.py**: contains functions to handle events from connections, sending and receiving messages
    *  **templates/chat**
        * **chat.html** 
    * **static/chat**
        * **styles.css**
        * **app.js**: handle the communication between frontend and backend, which will render sent/received messages 
* **feed**
    * **context_processor.py**: to populate the context (form to create new post) when a template is rendered with a request
    * **models.py**: create Post, Comment, Like models
    * **my_forms.py**: form to create a new post
    *  **urls.py**
    *  **views.py**: functions to handle creating new post, display list of posts, like and comment actions
    *  **templates/feed**
        * **index.html**: list of posts, this is the default routing when start to run the project 
        * **post.html**: a specific post 
        * **user_posts.html**: posts form a specific user
    * **static/feed**
        * **action.js**: handle like/ comment events.
    
### Requirements

In this project, some Python packages need to be installed to run the web application:
- djangorestframework
- channels
- channels-redis

To have these packages installed, run 
```sh
$ pip install -r requirements.txt 
```
### How to run
A Django Channels channel layer ( which allows multiple consumer instances to talk with each other, and with other parts of Django) that uses Redis as its backing store. To start a Redis server on port 6379, run the following command on another terminal:
```sh
$ docker run -p 6379:6379 -d redis:5
```
Then go to the project directory and run 
```sh
$ python manage.py runserver
```

