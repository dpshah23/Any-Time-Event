document.getElementById('eventForm').addEventListener('submit', function(event) {
    event.preventDefault();
    
    let isValid = true;
    const volunteerField = document.getElementById('requiredVolunteers');
    const contactField = document.getElementById('contactNo');
    const volunteerError = document.getElementById('volunteerError');
    const contactError = document.getElementById('contactError');
    
    volunteerError.style.display = 'none';
    contactError.style.display = 'none';

    if (volunteerField.value.length !== 10) {
        volunteerError.textContent = 'Required number of volunteers must be exactly 10 digits.';
        volunteerError.style.display = 'block';
        isValid = false;
    }

    if (contactField.value.length !== 10) {
        contactError.textContent = 'Contact number must be exactly 10 digits.';
        contactError.style.display = 'block';
        isValid = false;
    }

    if (isValid) {
        alert('Form submitted!');
    }
});
