document.addEventListener('DOMContentLoaded', function() {
    var today = new Date();
    var formattedToday = today.toISOString().split('T')[0];
    document.getElementById('date').min = formattedToday;

    document.getElementById('date').addEventListener('change', function() {
        var selectedDate = new Date(this.value);
        if (selectedDate < today) {
            this.value = formattedToday;
            alert('Please select a date that is today or in the future.');
        }
    });

    document.getElementById('eventForm').addEventListener('submit', function(event) {
        var contactNo = document.getElementById('contactNo').value;
        var contactError = document.getElementById('contactError');
        
        if (!/^\d{10}$/.test(contactNo)) {
            contactError.textContent = 'Contact number must be exactly 10 digits.';
            event.preventDefault();
        } else {
            contactError.textContent = '';
        }
    });
});
