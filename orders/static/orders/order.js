document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('repeatorder').addEventListener('click', () => {
        
        // load address form if chosen
        const select = document.querySelectorAll('#selectaddress');
        const form = document.getElementById('addressform').innerHTML;
        [...select].forEach((option) => {
            option.addEventListener('change', () => {
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
});