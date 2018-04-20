# ASSIGNMENT
### Git
You are **required** to use Github to complete this project
- [Git Workflow](docs/GIT_INFO.md)
- [Git Cheat Sheet](https://services.github.com/on-demand/downloads/github-git-cheat-sheet.pdf)

### Slack
You are **strongly encouraged** to use [Slack](https://principia-csci.slack.com/) to communicate with your group members to complete this project
- Use slack to arrange meeting times
- Use slack to share files quickly with teammates
- use slack to assign to-do lists

### Markdown
- you are to produce a detailed README.md file in your repository
  - [Learn Markdown](https://www.markdownguide.org/)
  - [Markdown Cheat Sheet](https://guides.github.com/pdfs/markdown-cheatsheet-online.pdf)

# Project Description
You are developing a Client/Server based chat application. The server program will reside on an ubuntu server that is accessible to your group through ssh: [your group server info](docs/UbuntuServer.md).

You must first start your chat server on cs-vus-00. Once the chat server is up and running you can start chat clients on other computers connected to the same network. The chat client will contact the chat server for authentication. **NO passwords** are to be sent **without** utilizing some **encryption** technique. If a client fails to authenticate 4 times, they will be locked out 5 minutes.

Once the client has been authenticated by the server, the server broadcasts a message to all other connected clients that the new user is online. The server must also send a message to the new user indicating all other users that are currently online.

Online users have the option of sending a broadcast message to all other online users or sending private messages directly to another user. If a user sends a message to a user that has signed off, the message is stored and delivered once that user signs back on. This message storage only applies to private messages.

When a user signs off, the server sends an update to all online users that the departing user is no longer online.

![ClientServer](docs/ClientServer.png)

## Server
* ##### Requirements
  - [x] maintain a list of usernames and passwords
    - [x] usernames and passwords read in from csv file when starting up
    - [x] passwords must be encrypted prior to transmission or saving
    - [x] new users can be added using a supporting program to encrypt passwords if desired
  - [x] authenticate users through client requests
    - [x] 4 failed authentications locks a user out for 5 minutes
  - [x] Once a user has been authenticated the server does the following
    - [x] sends a list of online users to the newly authenticated users
    - [x] sends a broadcast message to all others that the user is now online
  - [x] relays all broadcast messages to all other online users
  - [x] Once a user has been authenticated the server does the following
    - [x] sends a list of online users to the newly authenticated users
    - [x] sends a broadcast message to all others that the user is now online
  - [x] relays all broadcast messages to all other online users
  - [x] delivers private messages directly to specified user
    - [x] private messages for offline users are stored and delivered when that user comes back online
  - [x] control + c should terminate your server program without errors

* ##### Running your server program  
  * Server program must be run on the provided ubuntu server
  * **Use Port: 5003**
  * Use terminal or [Bitvise](https://www.bitvise.com/ssh-client-download) *(windows)* to logon to the ubuntu server
  * Clone your repository on [cs-vus-00](docs/UbuntuServer.md)
  ```terminal
    $ git clone https://github.com/PrincipiaCollege/3-pythonChat.git
    $ ./server.py or python3 server.py
  ```
  ```terminal
    use control + c to terminate your server program
  ```

## Client
* ##### Requirements
  - [x] provide interface to get username and password from users
    - [x] authenticate with the server
    - [x] repeat if needed and provide feedback to user
  - [x] display list of other online users when provided by server
  - [x] display any server provided messages
  - [x] provide method for sending broadcast messages
  - [x] provide method for sending private messages
  - [x] provide method for going offline and reporting this to the server
