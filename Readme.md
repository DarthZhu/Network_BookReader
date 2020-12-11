# README
## Function
+ turn page
+ turn chapter
+ goto chapter
+ goto page
+ bookmark
+ download
+ close
## Features
+ Multi-threading
+ GUI
## Design
1. Server
   
    Server stores user information, books and bookmarks. 

    Server handles requests from clients and sends results back to clients.

2. Client

    Client sends request to the server shows data in form of GUI.

3. Protocol

    Protocol is defined in `packet` and everytime server or client want to send, they have to send through `packet`.
## Protocol
`MessageType`: 

+ 0: initialize

+ 1-100: server action

+ 101-200: client action

+ 201-: error

`packet`: 

```|--MessageType(3 bytes)--|-------data(4093 bytes)-------|```

provides utilities:

+ packet to bytes with encoding "utf-8"

+ bytes to packet with decoding "utf-8"

+ packet to bytes without encoding (used when sending files)

+ bytes to packet without decoding (used when receiving files)
## Structure
```
|server
|---books(store books)
|---storage(store user information and bookmarks)
|---__init__.py: initialize and multi-threading
|---client_handler.py: handle and dispatch client request
|client
|---interfaces(GUI for client)
|---|---login_interface.py: client log in here
|---|---main_interface.py: client see this inferface after login
|---|---read_interface.py: book is shown on this interface
|---__init__.py: initialize client
|---mem.py: temporary memory for username and root window
|protocol
|---__init__.py: define MessageType and class packet
|utils
|---__init__.py: utility functions
|run_server.py: run this file to start server
|run_client.py: run this file to start client
```
## How to run
Run `python run_server.py` under root directory to start the server. Only one server can be started, others will be blocked due to port is occupied.

Run `python run_client.py` under root directory to start the GUI client. You can start multiple clients and log in as different users. The server can handle up to 5 clients at the same time.