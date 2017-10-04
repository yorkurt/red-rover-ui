
var maxPower = 0;
var heading = "None";
var power = 0;
var xHeading = 0;
var yHeading = 0;
var python = " ";
var armPos = "open";
var gripPos = "open";

function test(x, y){
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function(){
    if (this.readyState == 4 && this.status == 200) {
   	python = this.responseText;
	test(xHeading, yHeading);
    }
  }
  var requestString = "test.py?x=" + x + "&y=" + y + "&g=" + gripPos + "&a=" + armPos;
  xhttp.open("GET", requestString, true);
  xhttp.send();
}


function init(){
  var touchMe = document.getElementById('uiCanvas');
  var orbit = document.getElementById('powerCanvas');
  drawBorder();
  drawOrbit();
  touchMe.addEventListener("touchmove", draw, false);
  orbit.addEventListener("touchmove", drawPower, false);
  test(0, 0);
  updateInfo();
}

function drawPower(){
  var canvas = document.getElementById('powerCanvas');
  var x = event.touches[0].clientX;
  x = Math.min(250, Math.max(x, 50));
  maxPower = Math.round((x - 50) / 2);
  var y = 225 - Math.sqrt(Math.pow(150, 2) - Math.pow(x - 150, 2));
  clearCanvas(canvas);
  drawOrbit();
  drawCircle(canvas, x, y, 30, "#a2a8ae");
}

function clearCanvas(canvas){
  var ctx = canvas.getContext('2d');
  ctx.clearRect(0, 0, canvas.width, canvas.height);
}

function drawCircle(canvas, x, y, radius, color){
  var ctx = canvas.getContext('2d');
  ctx.beginPath();
  ctx.arc(x, y, radius, 0, 2*Math.PI);
  ctx.fillStyle = color;
  ctx.fill();
}

function drawOrbit(){
  var orbit = document.getElementById('powerCanvas');
  var oCtx = orbit.getContext('2d');
  oCtx.beginPath();
  oCtx.fillStyle = "#000000";
  oCtx.arc(orbit.width/2, (orbit.height/2)+150, 150, 0, 2*Math.PI, false);
  oCtx.fill();
  oCtx.beginPath();
  oCtx.fillStyle = "#ffffff";
  oCtx.arc(orbit.width/2, (orbit.height/2)+150, 149, 0, 2*Math.PI, false);
  oCtx.fill();
}
function drawBorder(){
  var canvas = document.getElementById('uiCanvas');
  if (canvas.getContext){
    var ctx = canvas.getContext('2d');
    ctx.beginPath();
    ctx.fillStyle = "#000000";
    ctx.arc(canvas.width/2, canvas.height/2, 100, 0, 2*Math.PI);
    ctx.fill();
    ctx.beginPath();
    ctx.fillStyle = "#ffffff";
    ctx.arc(canvas.width/2, canvas.height/2, 99, 0, 2*Math.PI);
    ctx.fill();
    ctx.beginPath();
    ctx.fillStyle = "#ff0000";
    ctx.arc(canvas.width/2, canvas.height/2, 45, 0, 2*Math.PI);
    ctx.fill();
    }
}

function getHeading(x, y){ //returns a string representing the rover's heading
  var ew = (x - 150) < 0 ? "W":"E";
  var ns =  (y - 150) < 0 ? "N":"S";
  return ns + ew;
}
function draw() {
  var canvas = document.getElementById('uiCanvas');
  var radius = 100;
  var lineLength = radius;
  if (canvas.getContext){
    var ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    drawBorder();
    ctx.beginPath();
    var x = event.touches[0].clientX;
    var y = event.touches[0].clientY - 150;
    var originX = canvas.width/2;
    var originY = canvas.height/2;
    x = x - originX;
    y = y - originY;
    var lineLength = Math.sqrt(Math.pow(x, 2) + Math.pow(y, 2));
    if (lineLength > radius){
      x = x / lineLength;
      y = y / lineLength;
      x = x*radius + originX;
      y = y*radius + originY;
    } else {
      x = event.touches[0].clientX;
      y = event.touches[0].clientY - 150;
    }
    ctx.arc(x, y, 30, 0, 2*Math.PI);
    ctx.fillStyle = "#a2a8ae";
    ctx.fill();
    power = ((lineLength > radius)?radius:lineLength) / radius;
    heading = getHeading(x, y);
    xHeading = Math.round(((x-150) /100) * maxPower);
    yHeading = Math.round(((y-150)/ 100) * maxPower);
    }
}

function updateInfo(){
  document.getElementById('info').innerHTML = "Throttle: " +
  maxPower + "% Current Power: " + Math.round(power * maxPower) +
  "% of Max Heading: " + heading + " Python Reponse: " + python;
  setTimeout(updateInfo, 100);
}
function toggleArm(){
  button = document.getElementById("arm");
  if (button.innerHTML == 'Open Arm')
    {
    button.innerHTML = "Close Arm";
    armPos = "open";		
    } else {
    button.innerHTML = "Open Arm";
    armPos = "closed";
    }
}
function toggleGrip(){
  button = document.getElementById('grip');
  if (button.innerHTML == "Open Grip") {
    button.innerHTML = "Close Grip";
    gripPos = "open";
    } else {
    button.innerHTML = "Open Grip";
    gripPos = "closed";
  }
}

