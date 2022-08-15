document.addEventListener('DOMContentLoaded', () => {
    [...document.querySelectorAll('.alert')].forEach( (alert) => {
        if(alert.innerHTML === '' || alert.innerHTML === null) {
            alert.style.display = 'none';
        } else {
            alert.style.display = 'block';
        }
    });
});