# client_ip_address
This is an application that serves an http endpoint that returns the clients ip address and an indication of the last time a request was received from that client ip address. 

## Tech used 
- Python
- Nginx
- Mongodb
- Docker

## To run the application

- enter docker compose up -d 
- Listing containers must show three containers running:   dockers-web-1, dockers-mongo-1 and dockers-backend-1. 
- After the application starts, navigate to http://localhost:80/api/myip
