const btn = document.querySelector('button');

function shortenURL() {
    const xhr = new XMLHttpRequest();
    const url = "http://localhost/api/shorten";  // TODO: put in config
    xhr.open('POST', url, true);
    xhr.setRequestHeader("Content-type", "application/json");

    const url_to_shorten = document.getElementById('url').value
    const payload = JSON.stringify({"url": url_to_shorten})

    xhr.onreadystatechange = function() {
        if (xhr.readyState == XMLHttpRequest.DONE) {
            data = JSON.parse(xhr.responseText)
            var msg = ""
            if (xhr.status == 400) {
                document.getElementById('msg').innerHTML = data['msg'];
            } else {
                const shorten_url = data['shorten_url']
                document.getElementById('msg').innerHTML =
                    url_to_shorten + " is converted to <a target='_blank' rel='noopener noreferrer' href='" + shorten_url + "'>" + shorten_url + "</a>";
            }
        }
    }
    xhr.send(payload)
}

btn.addEventListener('click', function(){
    shortenURL();
})