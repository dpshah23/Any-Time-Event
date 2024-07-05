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
    contactNoError.style.color = "red";
    contactNoError.style.marginTop = "15px";
    isValid = false;
  }

  if (password !== confirmPassword) {
    document.getElementById("passwordError").textContent = "Passwords do not match.";
    document.getElementById("confirmPasswordError").textContent = "Passwords do not match.";
    passwordError.style.color = "red";
    confirmPasswordError.style.color = "red";
    passwordError.style.marginTop = "15px";
    confirmPasswordError.style.marginTop = "15px";
    isValid = false;
  }

  return isValid;
}

document.getElementById("submitButton").addEventListener("click", function (event) {
  if (!validateForm()) {
    event.preventDefault();
  }
});
