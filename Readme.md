# README
## Function
+ turn page
+ turn chapter
+ goto chapter
+ goto page
+ bookmark
+ download
+ close
## Protocol
`packet`
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
|---__init__.py: 
|protocol
|---protocol.py: define MessageType and class packet
|utils
|---__init__.py: utility functions
|run_server.py: run this file to start server
|run_client.py: run this file to start client
```
