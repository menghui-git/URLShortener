const btn = document.querySelector('button');

function shortenURL() {
    const url_max_len = 200;
    const url_to_shorten = document.getElementById('url').value;
    const url_len = url_to_shorten.length;

    if (url_len == 0 || url_len > url_max_len) {
        document.getElementById('msg').innerHTML = "Please enter url (at most 200 characters)";
        return;
    }

    const xhr = new XMLHttpRequest();
    const url = "http://localhost/api/shorten";  // TODO: put in config
    xhr.open('POST', url, true);
    xhr.setRequestHeader("Content-type", "application/json");

    xhr.onreadystatechange = () => {
        if (xhr.readyState == XMLHttpRequest.DONE) {
            if (xhr.status == 503) {
                document.getElementById('msg').innerHTML =
                    "Your quota for shortening/redirecting URL service is over now.\n Please try it later.";
                return;
            }

            data = JSON.parse(xhr.responseText);
            if (xhr.status == 400) {
                document.getElementById('msg').innerHTML = data['msg'];
            } else {
                const shorten_url = data['shorten_url'];
                document.getElementById('msg').innerHTML =
                    url_to_shorten + " is converted to <a target='_blank' rel='noopener noreferrer' href='" + shorten_url + "'>" + shorten_url + "</a>";
            }
        }
    }
    const payload = JSON.stringify({"url": url_to_shorten});
    xhr.send(payload);
}

btn.addEventListener('click', shortenURL);