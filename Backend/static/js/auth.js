// ==========================================
// HOSTEL SCOUT Authentication JavaScript
// ==========================================


// ------------------------------------------
// ELEMENTS
// ------------------------------------------

const password =
document.getElementById("password");

const confirmPassword =
document.getElementById("confirm_password");

const strengthFill =
document.getElementById("strength-fill");

const strengthText =
document.getElementById("strength-text");

const passwordMatch =
document.getElementById("password-match");

const registerButton =
document.getElementById("register-btn");


// ------------------------------------------
// SHOW / HIDE PASSWORD
// ------------------------------------------

function togglePassword(id, eye){

    const input =
    document.getElementById(id);

    if(!input) return;

    if(input.type === "password"){

        input.type = "text";

        eye.innerHTML = "🙈";

    }

    else{

        input.type = "password";

        eye.innerHTML = "👁";

    }

}


// ------------------------------------------
// PASSWORD STRENGTH
// ------------------------------------------

if(password){

password.addEventListener("input", function(){

    let score = 0;

    const value = password.value;

    if(value.length >= 8)
        score++;

    if(/[A-Z]/.test(value))
        score++;

    if(/[a-z]/.test(value))
        score++;

    if(/[0-9]/.test(value))
        score++;

    if(/[^A-Za-z0-9]/.test(value))
        score++;

    const colors = [

        "#ef4444",

        "#f97316",

        "#eab308",

        "#22c55e",

        "#16a34a"

    ];

    const labels = [

        "Very Weak",

        "Weak",

        "Fair",

        "Strong",

        "Excellent"

    ];

    if(strengthFill){

        strengthFill.style.width =
        (score * 20) + "%";

        strengthFill.style.background =
        colors[score - 1] || "#e2e8f0";

    }

    if(strengthText){

        strengthText.innerHTML =
        labels[score - 1] || "";

    }

    checkPasswords();

});

}


// ------------------------------------------
// PASSWORD MATCH CHECK
// ------------------------------------------

function checkPasswords(){

    if(

        !password ||

        !confirmPassword ||

        !registerButton

    ){

        return;

    }

    if(confirmPassword.value.trim() === ""){

        if(passwordMatch){

            passwordMatch.innerHTML = "";

        }

        registerButton.disabled = true;

        return;

    }

    if(password.value === confirmPassword.value){

        if(passwordMatch){

            passwordMatch.innerHTML =
            "✔ Passwords Match";

            passwordMatch.style.color =
            "#16a34a";

        }

        registerButton.disabled = false;

    }

    else{

        if(passwordMatch){

            passwordMatch.innerHTML =
            "✖ Passwords Do Not Match";

            passwordMatch.style.color =
            "#dc2626";

        }

        registerButton.disabled = true;

    }

}

// ------------------------------------------
// PASSWORD EVENTS
// ------------------------------------------

if(password && confirmPassword){

    password.addEventListener(

        "keyup",

        checkPasswords

    );

    confirmPassword.addEventListener(

        "keyup",

        checkPasswords

    );

}



// ------------------------------------------
// BUTTON LOADING EFFECT
// ------------------------------------------

document.querySelectorAll(".auth-btn").forEach(

function(btn){

btn.addEventListener(

"click",

function(e){

    if(this.disabled){

        e.preventDefault();

        return;

    }

    const text =

    this.querySelector(".btn-text");

    if(text){

        text.innerHTML =

        "⏳ Please wait...";

    }

    this.style.opacity = ".85";

    this.style.pointerEvents = "none";

});

});



// ------------------------------------------
// AUTO HIDE FLASH MESSAGES
// ------------------------------------------

window.addEventListener(

"load",

function(){

const flashes =

document.querySelectorAll(".flash");

flashes.forEach(function(flash){

setTimeout(function(){

flash.style.transition =

"all .5s ease";

flash.style.opacity = "0";

flash.style.transform =

"translateY(-10px)";

setTimeout(function(){

flash.remove();

},500);

},4000);

});

});



// ------------------------------------------
// INPUT FOCUS EFFECT
// ------------------------------------------

document.querySelectorAll(

".auth-input"

).forEach(function(input){

input.addEventListener(

"focus",

function(){

this.style.borderColor =

"#2563eb";

this.style.boxShadow =

"0 0 0 4px rgba(37,99,235,.15)";

});

input.addEventListener(

"blur",

function(){

this.style.boxShadow = "none";

});

});

// ------------------------------------------
// PREVENT NULL ERRORS
// ------------------------------------------

document.addEventListener("DOMContentLoaded", function () {

    // Prevent accidental form submission with Enter
    // when passwords don't match

    const registerForm = document.querySelector("form");

    if (
        registerForm &&
        password &&
        confirmPassword &&
        registerButton
    ) {

        registerForm.addEventListener("submit", function (e) {

            // Run one last validation
            checkPasswords();

            if (registerButton.disabled) {

                e.preventDefault();

                alert("Passwords do not match.");

            }

        });

    }

});


// ------------------------------------------
// SUCCESS MESSAGE
// ------------------------------------------

console.log(
    "%cHOSTEL SCOUT Authentication Loaded",
    "color:#2563eb;font-size:14px;font-weight:bold;"
);


// ------------------------------------------
// END OF FILE
// ------------------------------------------