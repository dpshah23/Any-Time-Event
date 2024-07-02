document.getElementById('resetForm').addEventListener('submit', function(event) {
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
        this.submit();
    }
});
