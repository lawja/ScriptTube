// 2. This code loads the IFrame Player API code asynchronously.
var tag = document.createElement('script');


tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

// grabs the text from the search box
var val = document.getElementById("txtSearch").placeholder;

document.getElementById('iframe').src = "https://www.youtube.com/embed/EVT9BdD6KaY";

