console.log("JavaScript connected!")

const password = document.getElementById("password")
const button = document.getElementById("show-password")

const confirmDelete = document.querySelector(".delete-form");

if (button) {
    button.addEventListener("click", function() {

        if (password.type === "password") {
            password.type = "text";
            button.innerHTML = '<i class="fa-solid fa-eye-slash"></i>';
        }
        else {
            password.type = "password";
            button.innerHTML = '<i class="fa-solid fa-eye"></i>';
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