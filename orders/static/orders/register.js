document.addEventListener('DOMContentLoaded', () => {

    // add class to helptext lists
    document.querySelector('.helptext > ul').classList.add('list-group', 'list-group-flush');
    [...document.querySelectorAll('.helptext > ul > li')].forEach((li) => {
        li.classList.add('list-group-item', 'px-0');
        li.style.backgroundColor = '#9B9B96';
        li.style.color = '#EBEBE6';
    });


    if (document.getElementById('msg').innerHTML === "" || document.getElementById('msg').innerHTML === null) {
        document.getElementById('msg').style.display = "none";
    }

    // submit form
    document.getElementById('registerform').onsubmit = () => {
        fetch("/register", {
            method: "POST",
            credentials: 'same-origin',
            headers: {
                "X-CSRFToken": getCookie("csrftoken")
            },
            body: JSON.stringify({
                username: document.getElementById('id_username').value,
                password1: document.getElementById('id_password1').value,
                password2: document.getElementById('id_password2').value,
                first_name: document.getElementById('id_first_name').value,
                last_name: document.getElementById('id_last_name').value,
                email: document.getElementById('id_email').value
            }),
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            if(data.success === true){
                window.location.replace('/');
            } else {
                document.getElementById('msg').style.display = "block";
                document.getElementById('msg').innerHTML = data.msg;
                document.getElementById('msg').scrollIntoView({behavior: "smooth"});
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