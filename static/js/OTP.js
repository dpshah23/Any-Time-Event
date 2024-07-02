document.addEventListener("DOMContentLoaded", function() {
    const inputs = document.querySelectorAll('.inputs input');

    inputs.forEach((input, index) => {
        input.addEventListener('input', (e) => {
            const value = e.target.value;
            if (/^\d$/.test(value)) {
                if (index < inputs.length - 1) {
                    inputs[index + 1].focus();
                }
            } else {
                input.value = '';
                alert('Please enter only digits');
            }
        });

        input.addEventListener('keydown', (e) => {
            if (e.key === 'Backspace' && input.value === '' && index > 0) {
                inputs[index - 1].focus();
            }
        });
    });
});
