document.getElementById('resetForm').addEventListener('submit', function(event) {
    // Prevent form submission for validation checks
    event.preventDefault();

    const newPassword = document.getElementById('newPassword').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    const message = document.getElementById('message');

    if (newPassword.length < 8) {
        message.style.color = 'red';
        message.textContent = 'Password must be at least 8 characters long.';
    } else if (newPassword !== confirmPassword) {
        message.style.color = 'red';
        message.textContent = 'Passwords do not match.';
    } else {
        // Validation passed, allow form submission
        this.submit();  // Submit the form
    }
});
