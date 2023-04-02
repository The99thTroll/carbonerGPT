var title = document.getElementById("productTitle");

if(title != null){
    if(title.innerHTML.length > 100){
        title.innerHTML = title.innerHTML.substring(0, 100) + "...";
    }
    chrome.runtime.sendMessage({'data': title.innerHTML, 'id': "title"});

    var img = document.querySelector("#landingImage");
    console.log(img.src);
    chrome.runtime.sendMessage({'data': img.src, 'id': "SCRIPT"});
}