function validateForm() {
  const contactNo = document.getElementById("contact_no").value;
  const password = document.getElementById("password").value;
  const confirmPassword = document.getElementById("confirm-password").value;

  let isValid = true;

  document.getElementById("contactNoError").textContent = "";
  document.getElementById("passwordError").textContent = "";
  document.getElementById("confirmPasswordError").textContent = "";

  if (contactNo.length !== 10) {
    document.getElementById("contactNoError").textContent = "Contact number must be exactly 10 digits.";
    isValid = false;
  }

  if (password !== confirmPassword) {
    document.getElementById("passwordError").textContent = "Passwords do not match.";
    document.getElementById("confirmPasswordError").textContent = "Passwords do not match.";
    isValid = false;
  }

  return isValid;
}

document.getElementById("signupForm").addEventListener("submit", function (event) {
  if (!validateForm()) {
    event.preventDefault();
  }
});

function togglePassword(fieldId, icon) {
  const field = document.getElementById(fieldId);
  if (field.type === "password") {
    field.type = "text";
    icon.classList.replace("bx-hide", "bx-show");
  } else {
    field.type = "password";
    icon.classList.replace("bx-show", "bx-hide");
  }
}
