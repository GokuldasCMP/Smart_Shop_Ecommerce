var email1Error = document.getElementById('login-email-error');
var passwordError = document.getElementById('error');
var submit_Error = document.getElementById('login-submit-error');





function validateEmail1() {
    var email1 = document.getElementById('email1').value;
    if (email1.length == 0) {
        email1Error.innerHTML = 'email required';
        return false;
    }
    if (!email1.match(/^[A-Za-z\._\-[0-9]*[@][A-Za-z]*[\.][a-z]{2,4}$/)) {
        email1Error.innerHTML = 'email invalid'
        return false;
    }
    email1Error.innerHTML = '<i class="fa-solid fa-circle-check" style="color:seagreen;position: absolute;bottom: 7px;left: 88px;"></i>';
    return true;

}


function validatePassword() {
    var password = document.getElementById('password').value;
    if (password.length == 0) {
        passwordError.innerHTML = 'password required'
        return false;
    }
    
    passwordError.innerHTML = '<i class="fa-solid fa-circle-check" style="color:seagreen;position: absolute;bottom: 7px;left: 130px;" ></i>';
    return true;
}

function validateForm1() {
    if (!validateEmail1() || !validatePassword()) {
        submit_Error.style.display = 'block';
        submit_Error.innerHTML = 'please fix error to submit';
        setTimeout(function () { submit_Error.style.display = 'none'; }, 3000);
        return false;
    }
    return true;
}
