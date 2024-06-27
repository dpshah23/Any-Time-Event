document.addEventListener('DOMContentLoaded', function () {
  
    const togglePassword = document.getElementById('togglePassword');
    const passwordField = document.getElementById('passwordField');
  
    togglePassword.addEventListener('click', function () {
  
        const type = passwordField.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordField.setAttribute('type', type);
  
        this.classList.toggle('bx-hide');
        this.classList.toggle('bx-show');
    });
  });
  