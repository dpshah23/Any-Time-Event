document.getElementById('otpForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const otpInput = document.getElementById('otpInput').value;
    const message = document.getElementById('message');

    if (otpInput.length !== 6 || isNaN(otpInput)) {
        message.textContent = 'Please Enter a Valid 6-digit OTP.';
    } else {
        message.textContent = 'OTP Verified Successfully!';
        message.style.color = 'green';
    }
});
