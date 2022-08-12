document.addEventListener('DOMContentLoaded', () => {

    console.log(document.getElementById('msg').innerHTML);
    if (document.getElementById('msg').innerHTML === "" || document.getElementById('msg').innerHTML === null) {
        console.log('here');
        document.getElementById('msg').style.display = "none";
    }

    document.getElementById('loginform').onsubmit = () => {
        fetch("/login", {
            method: "POST",
            credentials: 'same-origin',
            headers: {
                "X-CSRFToken": getCookie("csrftoken")
            },
            body: JSON.stringify({
                username: document.getElementById('id_username').value,
                password: document.getElementById('id_password').value
            }),
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            if(data.success === true){
                window.location.replace('/');
            } else {
                document.getElementById('msg').style.display = "block";
                document.getElementById('msg').innerHTML = "Invalid username or password !!!";
            }
        });
        return false;
    }
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}