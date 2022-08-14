document.addEventListener('DOMContentLoaded', () => {

    // remove items from cart
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

    // add items to cart
    const addbuttons = document.querySelectorAll('.addcart');
    [...addbuttons].forEach(addbutton => {
        addbutton.addEventListener('click', () => {
            fetch(`/item/${addbutton.dataset.class}/${addbutton.dataset.id}`, {
                method: "PUT",
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
    if (placeorder !== null) {
        placeorder.addEventListener('click', () => {

            // load address form if chosen
            const select = document.querySelectorAll('#selectaddress');
            console.log(select);
            console.log("gereg");
            const form = document.getElementById('addressform').innerHTML;
            console.log(form);
            [...select].forEach((option) => {
                console.log(option.value);
                option.addEventListener('change', () => {
                    console.log(option.value);
                    if (option.value === "addaddress"){
                        document.getElementById('addressform').style.display = 'block';
                        document.getElementById('addressform').innerHTML = form;
                    } else {
                        document.getElementById('addressform').style.display = "none";              
                        document.getElementById('addressform').innerHTML = '';
                    }
                });
            });

            // press form submit button to place order
            document.getElementById('confirmorder').addEventListener('click', () => {
                document.getElementById('actualconfirmorder').click();
            }); 
        });
    }
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
