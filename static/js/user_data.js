document.getElementById('birthdate').addEventListener('change', function() {
    var birthdate = new Date(this.value);
    var minDate = new Date();
    minDate.setFullYear(minDate.getFullYear() - 16);

    if (birthdate > minDate) {
        alert('Please select a birthdate that makes you at least 16 years old.');
        this.value = '';
    }
});

document.getElementById('emergency_no').addEventListener('input', function() {
    var contactNo = this.value;
    if (contactNo.length !== 10) {
        this.setCustomValidity('Contact number must be exactly 10 digits.');
    } else {
        this.setCustomValidity('');
    }
});