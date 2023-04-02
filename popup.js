function initialize(){
	chrome.extension.getBackgroundPage().chrome.tabs.executeScript(null, {
		file: 'payload.js'
	});
}

window.addEventListener('load', async function (evt) {
	initialize();
});

chrome.runtime.onMessage.addListener(function (message) {
	if(message.id != "SCRIPT"){
		document.getElementById(message.id).innerHTML = message.data;
	}else{
		//whatever you want to do with the image URL
	}
	//make a fetch request and get the carbon footprint of the product
	fetch("https://api.example.com/footprint/" + message)
		.then(response => response.json())
		.then(data => {
			 return document.getElementById('carbon').innerHTML = data.carbon;
		});
});