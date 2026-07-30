console.log("JavaScript connected!")

const password = document.getElementById("password")
const confirmPassword = document.getElementById("confirm-password")
const button = document.getElementById("show-password")
const confirmPasswordButton = document.getElementById("show-confirm-password")


const confirmDelete = document.querySelector(".delete-form");
const confirmDeletePhoto = document.querySelectorAll(".delete-photo-form");
const confirmDeleteAccount = document.querySelector(".delete-account");

if (button) {
    button.addEventListener("click", function() {

        if (password.type === "password") {
            password.type = "text";
            button.innerHTML = "<i class='fa-solid fa-eye-slash'></i>";
        }
        else {
            password.type = "password";
            button.innerHTML = "<i class='fa-solid fa-eye'></i>";
        }
    });
}

if (confirmPasswordButton) {
    confirmPasswordButton.addEventListener("click", function(){
    
        if (confirmPassword.type === "password") {
            confirmPassword.type = "text";
            confirmPasswordButton.innerHTML = "<i class='fa-solid fa-eye-slash'></i>";
        }
        else {
            confirmPassword.type = "password";
            confirmPasswordButton.innerHTML = "<i class='fa-solid fa-eye'></i>";
        }
    });
}

if (confirmDelete) {
    confirmDelete.addEventListener("submit", function(event) {

        if (!confirm("Are you sure you want to delete this entry?")) {
            event.preventDefault();
        }
    });
};

if (confirmDeletePhoto) {
    confirmDeletePhoto.addEventListener("submit", function(event) {

        if (!confirm("Are you sure you want to delete this photo?")) {
            event.preventDefault();
        }
    });
}

if (confirmDeleteAccount) {
    confirmDeleteAccount.addEventListener("submit", function(event){
        if (!confirm("Are you sure you want to delete your entire account permanently? You will lose all logs and photos. This is NOT reversible.")) {
            event.preventDefault();
        }
    });
}

document.querySelectorAll("form", function() {
    form.addEventListener("submit", function() {
        sessionStorage.setItem("scrollPosition", window.scrollY);
    });
});

window.addEventListener("load", function() {
    const scrollPosition = sessionStorage.getItem("scrollPosition")

    if (scrollPosition) {
        setTimeout(() => {
            window.scrollTo(0, scrollPosition)
            sessionStorage.removeItem("scrollPosition")
        }, 100);
    }
});