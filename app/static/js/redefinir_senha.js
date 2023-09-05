const emailInput = document.getElementById('email');
const recuperarButton = document.getElementById('recuperar');

emailInput.addEventListener('input', toggleRecuperarButton);

function toggleRecuperarButton() {
    recuperarButton.disabled = emailInput.value.trim() === '';
    recuperarButton.style.backgroundColor = recuperarButton.disabled ? '#6B44C2' : '#6B44C2';
}