document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector("form");
    const contactNoField = document.getElementById("contact_no_2");
    const errorMessage = document.querySelector(".error-message");

    form.addEventListener("submit", function(event) {
        const contactNo = contactNoField.value.trim();
        const digitRegex = /^\d{10}$/;

        if (!digitRegex.test(contactNo)) {
            event.preventDefault();
            errorMessage.style.display = "block";
            contactNoField.focus();
        } else {
            errorMessage.style.display = "none";
        }
    });
});