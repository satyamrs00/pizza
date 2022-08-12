document.addEventListener('DOMContentLoaded', () => {

    document.getElementById('save').addEventListener('click', () => {
        document.getElementById('actualsave').click();
    });
    document.getElementById('addaddresssave').addEventListener('click', () => {
        document.getElementById('actualaddaddresssave').click();
    });
    
    document.getElementById('editaccountform').addEventListener('submit', () => {
        document.getElementById('accountmodal').style.display = "none";
        fetch("/account", {
            method: "PATCH",
            credentials: 'same-origin',
            headers: {
                "X-CSRFToken": getCookie("csrftoken")
            },
            body: JSON.stringify({
                username: document.getElementById('username').value,
                first_name: document.getElementById('first_name').value,
                last_name: document.getElementById('last_name').value,
                email: document.getElementById('email').value
            }),
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            if (data.error) {
                window.alert(data.error);
            }
            window.location.reload();
        });
        return false;
    });
})

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