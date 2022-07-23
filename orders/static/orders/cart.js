document.addEventListener('DOMContentLoaded', () => {
    const removebuttons = document.querySelectorAll('.removecart');
    [...removebuttons].forEach(removebutton => {
        removebutton.addEventListener('click', () => {
            console.log(removebutton.dataset.class);
            console.log(removebutton.dataset.id);
            fetch(`/item/${removebutton.dataset.class}/${removebutton.dataset.id}`, {
                method : "PATCH",
                credentials: 'same-origin',
                headers: {
                    "X-CSRFToken": getCookie("csrftoken")
                }
            })
            .then(response => response.json())
            .then(data => {
                console.log(data);
                window.location.reload();
            });
        });
    });
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}