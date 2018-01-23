REM this runds the node http server proxy with no caching and a redirect to the webcam, and starts the mjpg helper script
REM replace this with the IP of your webcam if you are using an MJPEG-only camera. If it supports static images, you dont need this file
start node mjpg.js
start http-server -C-1 -P http://172.16.0.53:8020 