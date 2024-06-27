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
  