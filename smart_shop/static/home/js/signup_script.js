var firstnameError = document.getElementById('first-name-error');
var lastnameError = document.getElementById('last-name-error');
var emailError = document.getElementById('email-error');
var phoneError = document.getElementById('phone-error');
var password1Error = document.getElementById('password1-error');
var confirmationError = document.getElementById('confirmation-error');
var submitError = document.getElementById('submit-error');



function validateFirstname() {
  var firstname = document.getElementById('firstname').value;
  if (firstname.length == 0) {
    firstnameError.innerHTML = 'firstname is required';
    return false;
  }
  if (!firstname.match(/^[A-Za-z]*$/)) {
    firstnameError.innerHTML = 'write first name';
    return false;
  }
  firstnameError.innerHTML = '<i class="fa-solid fa-circle-check" style="color:seagreen;"></i>';
  return true;
}
function validateLastname() {
  var lastname = document.getElementById('lastname').value;
  if (lastname.length == 0) {
    lastnameError.innerHTML = 'lastname is required';
    return false;
  }
  if (!lastname.match(/^[A-Za-z]*$/)) {
    lastnameError.innerHTML = 'write last name';
    return false;
  }
  lastnameError.innerHTML = '<i class="fa-solid fa-circle-check" style="color:seagreen;"></i>';
  return true;
}

function validateEmail() {
  var email = document.getElementById('email').value;
  if (email.length == 0) {
    emailError.innerHTML = 'email required';
    return false;
  }
  if (!email.match(/^[A-Za-z\._\-[0-9]*[@][A-Za-z]*[\.][a-z]{2,4}$/)) {
    emailError.innerHTML = 'email invalid'
    return false;
  }
  emailError.innerHTML = '<i class="fa-solid fa-circle-check" style="color:seagreen;"></i>';
  return true;

}

function validatePhone() {
  var phone = document.getElementById('phone').value;
  if (phone.length == 0) {
    phoneError.innerHTML = 'phone number is required';
    return false;
  }
  if (phone.length !== 10) {
    phoneError.innerHTML = 'phone number should 10 digits';
    return false;
  }
  if (!phone.match(/^[0-9]{10}$/)) {
    phoneError.innerHTML = 'only digits please';
    return false;
  }
  phoneError.innerHTML = '<i class="fa-solid fa-circle-check" style="color:seagreen;"></i>';
  return true;

}
function validatePassword1() {
  var password1 = document.getElementById('password1').value;
  if (password1.length == 0) {
    password1Error.innerHTML = 'password required'
    return false;
  }
  if (password1.length !== 6) {
    password1Error.innerHTML = 'should 6 characters ';
    return false;
  }
  // if (!password1.match(/^(?=.[A-Za-z])(?=.\d)[A-Za-z\d]{3,}$/)) {
  //   password1Error.innerHTML = 'Atleat one character and one number';
  //   return false;

  // }
  password1Error.innerHTML = '<i class="fa-solid fa-circle-check" style="color:seagreen;"></i>';
  return true;
}
function validateConfirmation() {
  var confirmation = document.getElementById('confirmation').value;
  if (confirmation.length == 0) {
    confirmationError.innerHTML = 'password required'
    return false;
  }
  if (confirmation.length !== 6) {
    confirmationError.innerHTML = 'password should 6 characters';
    return false;
  }
  // if (!confirmation.match(/^(?=.[A-Za-z])(?=.\d)[A-Za-z\d]{6,}$/)) {
  //   confirmationError.innerHTML = 'Atleat one character and one number';
  //   return false;
  // }
  confirmationError.innerHTML = '<i class="fa-solid fa-circle-check" style="color:seagreen;"></i>';
  return true;
}
function validateForm() {
  if (!validateFirstname() || !validateLastname() || !validateEmail() || !validatePhone() || !validatePassword1() || !validateConfirmation()) {
    submitError.style.display = 'block';
    submitError.innerHTML = 'please fix error to submit';
    setTimeout(function () { submitError.style.display = 'none'; }, 3000);
    return false;
  }
  return true;
}