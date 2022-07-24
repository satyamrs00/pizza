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

    const placeorder = document.getElementById('placeorder');
    placeorder.addEventListener('click', () => {
        fetch('/cart', {
            method: "PUT",
            credentials: 'same-origin',
            headers: {
                "X-CSRFToken": getCookie("csrftoken")
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);

            let modalcontentdiv = loadConfirmation(data);
            let modaldiv = document.getElementById('modal');
            modaldiv.appendChild(modalcontentdiv);
            modaldiv.style.display = "block";

            document.querySelector('.close').addEventListener('click', () => {
                modaldiv.style.display = "none";
                while(modaldiv.firstChild){
                    modaldiv.removeChild(modaldiv.lastChild);
                }
            });
            window.onclick = (event) => {
                if (event.target == modaldiv) {
                    modaldiv.style.display = "none";
                    while(modaldiv.firstChild){
                        modaldiv.removeChild(modaldiv.lastChild);
                    }
                }
            }

            
        });
    });
});

function loadConfirmation(data) {
    let modalcontentdiv = document.createElement('div');
    modalcontentdiv.setAttribute('class', 'modal-content');
    let closespan = document.createElement('span');
    closespan.setAttribute('class', 'close');
    closespan.innerHTML = '&times;';
    let pricediv = document.createElement('div');
    pricediv.innerHTML = `Total price for this order is ${data.price}`;
    let addresslabel = document.createElement('label');
    addresslabel.innerHTML = 'Address : <br><textarea name="address" cols="30" rows="10"></textarea>'
    let paymenth = document.createElement('div');
    paymenth.innerHTML = 'Choose a payment method : ';
    let paymentdiv = document.createElement('div');
    let label1 = document.createElement('label');
    label1.innerHTML = '<input type="radio" name="paymethod" value="creditcard">Credit Cart';
    let label2 = document.createElement('label');
    label2.innerHTML = '<input type="radio" name="paymethod" value="debitcard">Debit Cart';
    let label3 = document.createElement('label');
    label3.innerHTML = '<input type="radio" name="paymethod" value="netbanking">Net Banking';
    let label4 = document.createElement('label');
    label4.innerHTML = '<input type="radio" name="paymethod" value="cod">Cash on Delivery';
    paymentdiv.appendChild(label1);
    paymentdiv.appendChild(label2);
    paymentdiv.appendChild(label3);
    paymentdiv.appendChild(label4);
    let button = document.createElement('button');
    button.setAttribute('id', 'confirmorder');
    button.innerHTML = 'Confirm Order';
    modalcontentdiv.appendChild(closespan);
    modalcontentdiv.appendChild(pricediv);
    modalcontentdiv.appendChild(addresslabel);
    modalcontentdiv.appendChild(paymenth);
    modalcontentdiv.appendChild(paymentdiv);
    modalcontentdiv.appendChild(button);
    return modalcontentdiv;
}

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