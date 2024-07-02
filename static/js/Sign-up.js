function togglePassword(id, element) {
  const passwordField = document.getElementById(id);
  if (passwordField.type === "password") {
      passwordField.type = "text";
      element.classList.replace("bx-hide", "bx-show");
  } else {
      passwordField.type = "password";
      element.classList.replace("bx-show", "bx-hide");
  }
}

function validateForm() {
  const contactNo = document.getElementById("contact_no").value;
  const password = document.getElementById("password").value;
  const confirmPassword = document.getElementById("confirm-password").value;

  let isValid = true;

  document.getElementById("contactNoError").textContent = "";
  document.getElementById("passwordError").textContent = "";
  document.getElementById("confirmPasswordError").textContent = "";

  if (contactNo.length !== 10) {
      document.getElementById("contactNoError").textContent = "Contact number must be 10 digits.";
      isValid = false;
  }

  if (password !== confirmPassword) {
      document.getElementById("passwordError").textContent = "Passwords do not match.";
      document.getElementById("confirmPasswordError").textContent = "Passwords do not match.";
      isValid = false;
  }

  return isValid;
}
