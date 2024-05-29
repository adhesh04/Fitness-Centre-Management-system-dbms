const signInBtnLink = document.querySelector(".signInBtn-link");
const signUpBtnLink = document.querySelector(".signUpBtn-link");
const wrapper = document.querySelector(".wrapper");
const loginForm = document.getElementById("loginForm");
const signUpForm = document.querySelector(".form-wrapper.sign-up");
const message = document.getElementById("message");

signUpBtnLink.addEventListener("click", () => {
  wrapper.classList.add("active");
  message.textContent = ""; // Clear any previous messages
});

signInBtnLink.addEventListener("click", () => {
  wrapper.classList.remove("active");
  message.textContent = ""; // Clear any previous messages
});

loginForm.addEventListener("submit", (event) => {
  event.preventDefault(); // Prevent default form submission

  const username = loginForm.username.value;
  const password = loginForm.password.value;
  const existingUser = localStorage.getItem(username); // Check if user exists

  if (existingUser) {
    const userData = JSON.parse(existingUser);
    if (userData.password === password) {
      // Login successful
      message.textContent = "Login successful!";
      message.style.color = "green";
      // Redirect to profile page
      window.location.href = "main.html";
    } else {
      // Incorrect password
      message.textContent = "Incorrect username or password.";
      message.style.color = "red";
    }
  } else {
    // User does not exist, prompt to sign up
    message.textContent =
      "Account doesn't exist. Click the Sign Up button to create an account.";
    message.style.color = "blue";
  }
});

signUpForm.addEventListener("submit", (event) => {
  event.preventDefault(); // Prevent default form submission

  const newUsername = signUpForm.querySelector('input[type="text"]').value;
  const newPassword = signUpForm.querySelector('input[type="password"]').value;
  const existingUser = localStorage.getItem(newUsername); // Check if user already exists

  if (existingUser) {
    // User already exists
    message.textContent =
      "User already exists. Please choose a different username.";
    message.style.color = "red";
  } else {
    // Create new user
    const newUser = { username: newUsername, password: newPassword };
    localStorage.setItem(newUsername, JSON.stringify(newUser));
    message.textContent =
      "Account created successfully. You are now logged in.";
    message.style.color = "green";
    signUpForm.style.display = "none"; // Hide sign-up form
    loginForm.reset(); // Reset login form

    // Log in the user immediately after account creation
    // This assumes the login logic is the same as above
    window.location.href = "main.html";
  }
});
