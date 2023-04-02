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

var title = document.getElementById("productTitle");

if(title != null){
    var num = "23";

    if(title.innerHTML.length > 100){
        title.innerHTML = title.innerHTML.substring(0, 100) + "...";
    }

    console.log(title.innerHTML.substring(0,7));
    if(title.innerHTML.substring(0,1) == " "){
        num = Math.round((Math.random() * 19 + 2)*100)/100;
    }

    chrome.runtime.sendMessage({'data': title.innerHTML, 'id': "title"});

    var middleCol = document.querySelector("#centerCol");

    const parentDiv = document.createElement("div");
    parentDiv.style.display = "flex";
    parentDiv.style.flexDirection = "row";

    const footprintIng = document.createElement("img");
    footprintIng.src = "https://i.imgur.com/dMWsNce.png";
    footprintIng.width = 25;
    footprintIng.height = 25;
    parentDiv.appendChild(footprintIng);

    const subText = document.createElement("h3");
    const childText = document.createTextNode("Carbon Footprint: " + num + " kg");
    subText.appendChild(childText)
    parentDiv.appendChild(subText);

    middleCol.insertBefore(parentDiv, middleCol.children[6]);

    var img = document.querySelector("#landingImage");
    console.log(img.src);
    chrome.runtime.sendMessage({'data': img.src, 'id': "SCRIPT"});
}