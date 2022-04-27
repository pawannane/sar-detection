// Copyright (c) 2019 ml5
//
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

/* ===
ml5 Example
Real time Object Detection using objectDetector
=== */

let objectDetector;
let status;
let objects = [];
let video;
let canvas, ctx;
const width = 640;
const height = 480;
//let canvas = document.querySelector("#canvas");

//const TelegramBot = require('node-telegram-bot-api');

async function make() {
  // get the video
  video = await getVideo();
  objectDetector = await ml5.objectDetector('cocossd', startDetecting)
  canvas = createCanvas(width, height);
  ctx = canvas.getContext('2d');
}

// when the dom is loaded, call make();
window.addEventListener('DOMContentLoaded', function () {
  make();
});

function startDetecting() {
  console.log('model ready')
  detect();
}

function detect() {
  objectDetector.detect(video, function (err, results) {
    if (err) {
      console.log(err);
      return
    }
    objects = results;
    console.log(objects);
    //console.log(video)
    // canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);
    // let image_data_url = canvas.toDataURL('image/jpeg');

    // // data url of the image
    // console.log(image_data_url);
    if (objects) {
      draw();
    }

    detect();
  });
}

function draw() {
  // Clear part of the canvas
  ctx.fillStyle = "#000000"
  ctx.fillRect(0, 0, width, height);

  ctx.drawImage(video, 0, 0);
  for (let i = 0; i < objects.length; i += 1) {

    ctx.font = "16px Arial";
    ctx.fillStyle = "orange";
    ctx.fillText(objects[i].label, objects[i].x + 4, objects[i].y + 16);

    ctx.beginPath();
    ctx.rect(objects[i].x, objects[i].y, objects[i].width, objects[i].height);
    ctx.strokeStyle = "orange";
    ctx.stroke();
    ctx.closePath();
  }
  //canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);

  if (objects.length > 0 && objects[0].label == "person") {
    let image_data_url = canvas.toDataURL('image/jpeg');



    // // data url of the image
    console.log(image_data_url);

    //var blob = base64ToBlob(image_data_url.slice(23), 'image/jpeg')

    //var formData = new FormData();
    //formData.append('picture', image_data_url)

    $.ajax({
      url: "http://127.0.0.1:5000/telebot",
      type: "POST",
      cache: false,
      contentType: false,
      processData: false,
      data: image_data_url
    })
      .done(function (e) {
        alert('done!');
      })

    setTimeout(function () {
      //your code to be executed after 1 second
    }, 5000);
  }


}

// Helper Functions
async function getVideo() {
  // Grab elements, create settings, etc.
  const videoElement = document.createElement('video');
  videoElement.setAttribute("style", "display: none;");
  videoElement.width = width;
  videoElement.height = height;
  document.body.appendChild(videoElement);

  // Create a webcam capture
  const capture = await navigator.mediaDevices.getUserMedia({ video: true })
  videoElement.srcObject = capture;
  videoElement.play();

  return videoElement
}

function createCanvas(w, h) {
  const canvas = document.createElement("canvas");
  canvas.width = w;
  canvas.height = h;
  document.body.appendChild(canvas);
  return canvas;
}

function base64ToBlob(base64, mime) {
  mime = mime || '';
  var sliceSize = 1024;
  var byteChars = window.atob(base64);
  var byteArrays = [];

  for (var offset = 0, len = byteChars.length; offset < len; offset += sliceSize) {
    var slice = byteChars.slice(offset, offset + sliceSize);

    var byteNumbers = new Array(slice.length);
    for (var i = 0; i < slice.length; i++) {
      byteNumbers[i] = slice.charCodeAt(i);
    }

    var byteArray = new Uint8Array(byteNumbers);

    byteArrays.push(byteArray);
  }

  return new Blob(byteArrays, { type: mime });
}