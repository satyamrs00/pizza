var max;

document.addEventListener('DOMContentLoaded',() => {
    let addbuttons = document.getElementsByClassName('addbutton');
    [...addbuttons].forEach((addbutton) => {
        addbutton.onclick = () => {
            fetch(`/item/${addbutton.dataset.item}/${addbutton.getAttribute('id').replace( /^\D+/g, '')}`, {
                method: "GET",
                credentials: 'same-origin',
                headers: {
                    "X-CSRFToken": getCookie("csrftoken")
                }
            })
            .then(response => response.json())
            .then(data => {
                console.log(data);
                let modalcontentdiv = loadcartform(data, addbutton);
                let modaldiv = document.getElementById('modal');
                modaldiv.appendChild(modalcontentdiv);
                modaldiv.style.display = "block";

                let pprice = 0;
                let eprice = 0;
                let confirmationdiv = document.getElementById('priceconfirmation');
                confirmationdiv.innerHTML = `Price for this item will be : ${pprice + eprice}`;

                if(data.sizeoptions === true){
                    if (data.missingsize === null){
                        document.getElementById('small').addEventListener('click', () => {
                            pprice = parseFloat(data.smallprice);
                            confirmationdiv.innerHTML = `Price for this item will be : ${pprice + eprice}`;
                        })
                        document.getElementById('large').addEventListener('click', () => {
                            pprice = parseFloat(data.largeprice);
                            confirmationdiv.innerHTML = `Price for this item will be : ${pprice + eprice}`;
                        })
                    } else if (data.missingsize === "small"){
                        pprice = parseFloat(data.largeprice);
                        confirmationdiv.innerHTML = `Price for this item will be : ${pprice + eprice}`;  
                    } else if (data.missingsize === "large"){
                        pprice = parseFloat(data.smallprice);
                        confirmationdiv.innerHTML = `Price for this item will be : ${pprice + eprice}`;  
                    }
                } else {
                    pprice = parseFloat(data.price);
                }

                let before = document.querySelectorAll(`input[name="${data.extrastype}"]:checked`).length
                document.getElementById('cartform').addEventListener('click', (e) => {
                    var checks = document.querySelectorAll(`.${data.extrastype}`);
                    if (nodelist_contains(checks, e.target)){
                        let after = document.querySelectorAll(`input[name="${data.extrastype}"]:checked`).length
                        let extraid = parseInt(e.target.value.replace( /^\D+/g, ''));
                        var tmp = 0;
                        data.extras.forEach(extra => tmp = extra.id === extraid ? parseFloat(extra.price) : tmp);
                        if (before < after){
                            eprice += tmp;
                        } else if (before > after){
                            eprice -= tmp;
                        }
                        before = after;
                        confirmationdiv.innerHTML = `Price for this item will be : ${pprice + eprice}`;
                    }
                });
                document.getElementById('cartform').onsubmit = () => {
                    if (data.sizeoptions === true && data.missingsize == null && document.querySelector('input[name="size"]:checked') === null){
                        document.getElementById('msg').innerHTML = "select a size before adding to cart";
                        return false;
                    }
                    if (data.extrasoption === true && data.extrastype === "Toppings" && document.querySelectorAll(`.${data.extrastype}:checked`).length != data.extrasamount){
                        document.getElementById('msg').innerHTML = `select ${data.extrasamount} toppings before adding to cart`;
                        return false;
                    }
                }

                confirmationdiv.innerHTML = `Price for this item will be : ${pprice + eprice}`;

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

                if(data.extrastype === "Toppings"){
                    var checks = document.querySelectorAll(`.${data.extrastype}`);
                    max = data.extrasamount;
                    for (var i = 0; i < checks.length; i++){
                        checks[i].onclick = selectiveCheck;
                    }
                }
            });
        }
    });
})

function loadcartform(data, addbutton){
    // let modaldiv = document.createElement('div');
    // modaldiv.classList.add('modal');
    let modalcontentdiv = document.createElement('div');
    modalcontentdiv.classList.add('modal-content')
    let close = document.createElement('span');
    close.classList.add('close');
    close.innerHTML = '&times;';
    let name = document.createElement('div');
    name.innerHTML = data.name;
    let form = document.createElement('form');
    form.setAttribute('action', `/item/${addbutton.dataset.item}/${addbutton.getAttribute('id').replace( /^\D+/g, '')}`);
    form.setAttribute('method', 'post');
    form.setAttribute('id', 'cartform');
    let csrfinput = document.createElement('input');
    csrfinput.setAttribute('type', 'hidden');
    csrfinput.setAttribute('name', 'csrfmiddlewaretoken');
    csrfinput.setAttribute('value', getCookie('csrftoken'));
    form.appendChild(csrfinput);

    if (data.sizeoptions === true){
        if (data.missingsize === null){
            let sizeh = document.createElement('div');
            sizeh.innerHTML = 'Select Size';
            let label1 = document.createElement('label');
            let sizeinput1 = document.createElement('input');
            sizeinput1.setAttribute('type', 'radio');
            sizeinput1.setAttribute('name', 'size');
            sizeinput1.setAttribute('value', 'small');
            sizeinput1.setAttribute('id', 'small');
            label1.appendChild(sizeinput1);
            label1.innerHTML += 'Small';
            let br1 = document.createElement('br');
            let label2 = document.createElement('label');
            let sizeinput2 = document.createElement('input');
            sizeinput2.setAttribute('type', 'radio');
            sizeinput2.setAttribute('name', 'size');
            sizeinput2.setAttribute('value', 'large');
            sizeinput2.setAttribute('id', 'large');
            label2.appendChild(sizeinput2);
            label2.innerHTML += 'Large';
            let br2 = document.createElement('br');
    
            form.appendChild(sizeh);
            form.appendChild(label1);
            form.appendChild(br1);
            form.appendChild(label2);
            form.appendChild(br2);
        } else {
            let size = document.createElement('input');
            size.setAttribute('type', 'hidden');
            size.setAttribute('name', 'size');

            if(data.missingsize === "small"){
                size.setAttribute('value', 'large');
                size.setAttribute('id', 'large');
            } else if (data.missingsize === "large"){
                size.setAttribute('value', 'small');
                size.setAttribute('id', 'small');
            }
            form.appendChild(size);
        }
    }

    if (data.extrasoption === true){
        let extrah = document.createElement('div');
        extrah.innerHTML = `Select ${data.extrastype}`;
        if(data.extrastype === "Toppings"){
            extrah.innerHTML += `<br> select ${data.extrasamount} items`;
        }else {
            extrah.innerHTML += `<br>`;
        }
        form.appendChild(extrah);

        for (let i = 0; i < data.extras.length; i++){
            let elabel = document.createElement('label');
            let einput = document.createElement('input');
            einput.setAttribute('type', 'checkbox');
            einput.classList.add(data.extrastype);
            einput.setAttribute('name', data.extrastype);
            einput.setAttribute('value', `${data.extrastype}${data.extras[i].id}`);
            elabel.appendChild(einput);
            elabel.innerHTML += data.extras[i].name;
            let pricespan = document.createElement('span');
            if (data.extras[i].price != 0){
                pricespan.innerHTML = data.extras[i].price;
            }
            elabel.appendChild(pricespan);
            let br = document.createElement('br');
            form.appendChild(elabel);
            form.appendChild(br);
        }
    }
    let confirmationdiv = document.createElement('div');
    confirmationdiv.setAttribute('id', 'priceconfirmation');
    form.appendChild(confirmationdiv);
    let msg = document.createElement('div');
    msg.setAttribute('id', 'msg');
    form.appendChild(msg);
    let submitbutton = document.createElement('input');
    submitbutton.setAttribute('type', 'submit');
    submitbutton.setAttribute('value', 'Save');
    form.appendChild(submitbutton);
    modalcontentdiv.appendChild(name);
    modalcontentdiv.appendChild(close);
    modalcontentdiv.appendChild(form);
    // modaldiv.appendChild(modalcontentdiv);
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

function selectiveCheck(event) {
    var checkedChecks = document.querySelectorAll(".Toppings:checked");
    if (checkedChecks.length >= max + 1){
        return false;
    }
}

function nodelist_contains(nodelist, obj) {
    if (-1 < Array.from (nodelist).indexOf (obj))
        return true;
  
    return false;
} 

function getcheckedboxes(checkboxname){
    let checkboxes = document.getElementsByName(checkboxname);
    let checkedcheckboxes = [];
    for(let i = 0; i < checkboxes.length ; i++){
        if(checkboxes[i].checked){
            checkedcheckboxes.push(checkboxes[i]);
        }
    }
    return checkedcheckboxes;
}