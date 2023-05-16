# network-servers

# Web Server & Client & Pdp Pinger


## Description
A multi-threaded web server that interacts with any standard web clients using HTTP and displays the essential connection parameters.

## Functionality
* Multi-threaded server that handles multiple requests concurrently.
* Server is assumed to work only with HTTP get messages.
* Port number can be provided as an argument while running the program, otherwise default port number of 8080 is assigned.
* Server can handle incoming client requests and display essential client details.
* If no file is requested, then the server uses the default file to response.
* If the file requested by the client is not in the server, then it responses with “HTTP/1.1 404 Not Found”.
* If the file requested by the server is in the server, then it responses with “HTTP/1.1 200 OK”.
* Client connects the server and requests file to the server.
* Client displays the status and contents of the file requested.
* Client also displays essential server details.
