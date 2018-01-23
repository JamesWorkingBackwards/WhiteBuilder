// This utility is for WhiteBuilding using WebCams that don't support still images, only MJPEG streams.
// It continuously grabs a still image from an MJPEG IP endpoint and write it to a local file
// Where WhiteBuilderMain.html can reference it
// Don't need this at all if your WebCam supports single images (these you can reference directly from WhiteBuilderMain)
// Tested with the iOS IP Cam app and an old iPhone as the webcam
// Use in conjunction with 'start.cmd' and the node http-server proxy https://www.npmjs.com/package/http-server

var mjpeg2jpegs = require("mjpeg2jpegs");
var fs = require("fs");
var http = require("http");


var counter = 0;


    
    //replace with the properties of your webcam
    http.request({
        hostname: "172.16.0.53",
        port: 8020,
        path: "/videoView"
    }, mjpeg2jpegs(function (res) {
        var img = [];

        res.on("imageHeader", function (header) {
            //console.log("Image header: ", header);
            img = [];
        });
        res.on("imageData", function (data) {
            console.log("Image data: ", data.length);
            img.push(data);
        });
        res.on("imageEnd", function () {
            //console.log("Image end");
            //console.log(img.length);
            counter++;
            if (counter == 1) {


                    fs.writeFile('wbcapture.jpg', Buffer.concat(img), function (err) {

                        console.log('wrote file');
                        counter = 0;


                    });

            }

        });
    })).end();

