# README
* Principia College
* Computer Networking
* Spring 2018
* Group 3 - [Github Repo](https://github.com/PrincipiaCollege/3-pythonChat.git)

#### Developers
* Jonathan Ansumana
* Bjorn Mathisen
* Lee Tarnow


#### Project Requirements
 - yMySQL library
 - PyJWT library - [Documentation](https://pyjwt.readthedocs.io/en/latest/)

You can install these dependencies in the commandline window by typing in:

```
pip install PyMySQL
pip install PyJWT
```
***
#### Installation Instructions

* Copy the pythonChat.zip and extract all the contents to your desired folder.
* To start the server, simply run server.py in a command line console.
* To start the client, simply run the client.py in a command console or double click the file assuming python 3.5< is installed.
After that a GUI login interface will popup, simply log in with the supplied account or create your own.

```
username: username
password: username
OR
username: wef
password: wef
```

#### Usage and Commands <client>

Once you have registered an account go ahead and log in. A new window should appear, on the left is the window where all the current chats are displayed.
On your right is a window with the current logged in users.

To send a message simply type it in the box in the bottom of the screen and hit enter. Your message will now be broadcasted to all currently online users.

To send a private message: `/private <username> <message>` or `/message <username> <message>`.

#### Usage and Commands <server>

The server will start automatically once you start the server.py script. No additional arguments are required.

To stop the server, either exit out of the console window by hitting the `X` button or by using `CTRL+C`
