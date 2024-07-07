document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector("form");
    const contactNoField = document.getElementById("contact_no_2");

    form.addEventListener("submit", function(event) {
        const contactNo = contactNoField.value;

        if (contactNo.length !== 10) {
            event.preventDefault();
            alert("Alternate Contact No. should be exactly 10 digits.");
            contactNoField.focus();
        }
    });
});
