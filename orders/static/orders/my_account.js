document.addEventListener('DOMContentLoaded', () => {

    // revert any changes it may have been done to address form
    document.getElementById('addaddress').addEventListener('click', () => {
        let form = document.querySelector('.addressform-imp');
        form.setAttribute('id', 'addaddressform');
        form.reset();
    });

    // fill address form with existing address and let user change it
    const editaddresses = document.querySelectorAll('.editaddress');
    [...editaddresses].forEach( (button) => {
        button.addEventListener('click', () => {
            fetch(`/address/${button.dataset.id}`, {
                method: 'GET',
                credentials: 'same-origin',
                headers: {
                    "X-CSRFToken": getCookie("csrftoken")
                }
            })
            .then(response => response.json())
            .then(data => {
                document.querySelector('.addressform-imp').setAttribute('id', 'editaddressform');

                document.getElementById('id_name').value = data.name;
                document.getElementById('id_addressline').value = data.addressline;
                document.getElementById('id_city').value = data.city;
                document.getElementById('id_state').value = data.state;
                document.getElementById('id_country').value = data.country;
                document.getElementById('id_pin').value = data.pin;
                document.getElementById('id_phone').value = data.phone;

                document.getElementById('editaddressform').onsubmit = () => {
                    fetch(`/account`, {
                        method: 'PUT',
                        body: JSON.stringify({
                            id : button.dataset.id,
                            name : document.getElementById('id_name').value,
                            addressline : document.getElementById('id_addressline').value,
                            city : document.getElementById('id_city').value,
                            state : document.getElementById('id_state').value,
                            country : document.getElementById('id_country').value,
                            pin : document.getElementById('id_pin').value,
                            phone : document.getElementById('id_phone').value
                        }),
                        credentials: 'same-origin',
                        headers: {
                            'X-CSRFToken': getCookie('csrftoken')
                        }
                    })
                    .then(response => response.json())
                    .then(data => {
                        console.log(data);
                        if (data.success === true) {
                            window.location.reload();
                        }
                    });
                    return false;
                }

                document.getElementById('deleteaddress').addEventListener('click', () => {
                    fetch('/account', {
                        method: 'DELETE',
                        credentials: 'same-origin',
                        headers: {
                            'X-CSRFToken': getCookie('csrftoken')
                        },
                        body: JSON.stringify({
                            id: button.dataset.id
                        })
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success === true) {
                            window.location.reload();
                        }
                    })
                });
            });
        });
    });

    // click actual submit button to submit form
    document.getElementById('save').addEventListener('click', () => {
        document.getElementById('actualsave').click();
    });
    document.getElementById('addaddresssave').addEventListener('click', () => {
        document.getElementById('actualaddaddresssave').click();
    });

    document.getElementById('edit').onclick = () => {
        if (document.getElementById('accountmsg').innerHTML === '' || document.getElementById('accountmsg').innerHTML === null){
            document.getElementById('accountmsg').style.display = 'none';
        }
    }
    
    // send edit account details request
    document.getElementById('editaccountform').onsubmit = () => {
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
            if(data.success === true) {
                console.log('reload');
                window.location.reload();
            } else {
                console.log('error');
                document.getElementById('accountmsg').style.display = "block";
                document.getElementById('accountmsg').innerHTML = data.error;
                document.getElementById('accountmsg').scrollIntoView({behavior: "smooth"});
            }
        });
        console.log('dont submit');
        return false;
    };
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