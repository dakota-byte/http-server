# http-server

A simple HTTP server written in python. This was originally written following along [CodeCrafters](https://app.codecrafters.io/courses/http-server/introduction) "Build your own HTTP server" challenge. 

### Testing

To test it out, try running the following:

`python server.py --direction ./store/`

and in another terminal

`curl -v POST http://localhost:4221/files/test -H "Content-Length: 5" -H "Content-Type: application/octet-stream" -d 'hello'`

this demonstrates a POST request to a HTTP server!

### Features from the challenge:

- /echo/ endpoint
- /user-agent endpoint
- GET /files/
- POST /files/
- gzip compression

### Other features I've added as per RFC 2616 Hypertext Transfer Protocol -- HTTP/1.1:

- N/A