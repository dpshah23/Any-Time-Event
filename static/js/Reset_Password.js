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
        message.style.color = 'green';
        message.textContent = 'Password reset successfully!';
        
    }
});

document.getElementById('toggleNewPassword').addEventListener('click', function() {
    const passwordField = document.getElementById('newPassword');
    togglePasswordVisibility(passwordField, this);
});

document.getElementById('toggleConfirmPassword').addEventListener('click', function() {
    const passwordField = document.getElementById('confirmPassword');
    togglePasswordVisibility(passwordField, this);
});

function togglePasswordVisibility(passwordField, toggleIcon) {
    if (passwordField.type === 'password') {
        passwordField.type = 'text';
        toggleIcon.classList.replace('bx-hide', 'bx-show');
    } else {
        passwordField.type = 'password';
        toggleIcon.classList.replace('bx-show', 'bx-hide');
    }
}
