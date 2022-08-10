document.addEventListener('DOMContentLoaded', () => {
    const removebuttons = document.querySelectorAll('.removecart');
    [...removebuttons].forEach(removebutton => {
        removebutton.addEventListener('click', () => {
            fetch(`/item/${removebutton.dataset.class}/${removebutton.dataset.id}`, {
                method: "PATCH",
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

    const placeorder = document.getElementById('placeorder');
    placeorder.addEventListener('click', () => {

        const select = document.getElementById('selectaddress');
        const form = document.getElementById('addressform').innerHTML;
        select.addEventListener('change', () => {
            if (select.value === "addaddress"){
                document.getElementById('addressform').style.display = 'block';
                document.getElementById('addressform').innerHTML = form;
            } else {
                document.getElementById('addressform').style.display = "none";              
                document.getElementById('addressform').innerHTML = '';
            }
        });

        document.getElementById('orderform').onsubmit = () => {
            if(document.querySelector('input[name="paymethod"]:checked') === null){
                document.getElementById('msg').innerHTML = "Select a payment method";
                return false;
            }
            return true;
        }
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
