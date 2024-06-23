### Here are a variety of curl commands you should test this server against, followed by their expected output

### Some tests are in order (Such as POSTing and then GETting)

curl -v http://localhost:4221/

"HTTP/1.1 200 OK\r\n\r\n"

curl -v http://localhost:4221/pineapple

"HTTP/1.1 404 Not Found\r\n\r\n"

curl -v http://localhost:4221/echo/strawberry

"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 10\r\n\r\nstrawberry"

curl -v http://localhost:4221/user-agent -H "User-Agent: apple/mango-mango"

"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 17\r\n\r\napple/mango-mango"

(concurrent connections) curl -v http://localhost:4221/

(received x amount of times) "HTTP/1.1 200 OK\r\n\r\n"

curl -v POST http://localhost:4221/files/pineapple_grape_grape_pineapple -H "Content-Length: 69" -H "Content-Type: application/octet-stream" -d 'blueberry blueberry orange mango raspberry blueberry banana blueberry'

curl -v -X POST http://localhost:4221/files/pineapple_grape_grape_pineapple -H "ConteNt-LEngth:69" -H "Content-type :application/octet-stream" -d 'blueberry blueberry orange mango raspberry blueberry banana blueberry' (Testing case insensitivty)

"HTTP/1.1 201 Created\r\n\r\n"

curl -v http://localhost:4221/files/pineapple_grape_grape_pineapple

"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: 69\r\n\r\nblueberry blueberry orange mango raspberry blueberry banana blueberry"

curl -v -H "Accept-Encoding: gzip" http://localhost:4221/echo/abc | hexdump -C

HTTP/1.1 200 OK
Content-Encoding: gzip
Content-Type: text/plain
Content-Length: 23

1F 8B 08 00 00 00 00 00
00 03 4B 4C 4A 06 00 C2
41 24 35 03 00 00 00

curl -v -H "Accept-Encoding: this-isnt-real-lol" http://localhost:4221/echo/abc

HTTP/1.1 406 Not Acceptable
Content-Type: text/plain

curl -v -X HEAD http://localhost:4221/files/pineapple_grape_grape_pineapple

"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: 69\r\n\r\n"