window.onload = function () {
  // Get the registration form
  var form = document.getElementById("registrationForm");

  // Add submit event listener to the form
  form.addEventListener("submit", function (event) {
    // Prevent the default form submission behavior
    event.preventDefault();

    // Redirect to success.html after form submission
    window.location.href = "success.html";
  });
};
