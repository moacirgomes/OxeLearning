// JavaScript functions for interacting with the elements
// and handling events on the page

const emailInput = document.getElementById("email");
const passwordInput = document.getElementById("password");
const entrarButton = document.getElementById("entrar");

emailInput.addEventListener("input", toggleEntrarButton);
passwordInput.addEventListener("input", toggleEntrarButton);

function toggleEntrarButton() {
    entrarButton.disabled = emailInput.value.trim() === "" || passwordInput.value.trim() === "";
    entrarButton.style.backgroundColor = entrarButton.disabled ? "#6B44C2" : "#6B44C2";
}

const passwordToggle = document.querySelector(".password-toggle");

passwordToggle.addEventListener("click", function () {
    const type = passwordInput.getAttribute("type") === "password" ? "text" : "password";
    passwordInput.setAttribute("type", type);
    passwordToggle.querySelector("i").classList.toggle("fa-eye");
    passwordToggle.querySelector("i").classList.toggle("fa-eye-slash");
});
