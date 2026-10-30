console.log("JavaScript connected!")

const password = document.getElementById("password")
const confirmPassword = document.getElementById("confirm-password")
const button = document.getElementById("show-password")
const confirmPasswordButton = document.getElementById("show-confirm-password")


const confirmDeleteRun = document.querySelectorAll(".delete-run-form");
const confirmDeletePhoto = document.querySelectorAll(".delete-photo-form");
const confirmDeleteAccount = document.querySelector(".delete-account");


function editRun(id) {
    console.log("Edit clicked:", id);
    
    const button = document.getElementById(`edit-button-${id}`);
    const row = document.getElementById(`run-${id}`);

    const milesInput = row.querySelector('input[name="miles"]');
    const runDateInput = row.querySelector('input[name="run_date"]');
    const activityInput = row.querySelector('select[name="activity"]');

    if (button.textContent.trim() === "Edit") {
        row.dataset.originalMiles = milesInput.value;
        row.dataset.originalDate = runDateInput.value;
        row.dataset.originalActivity = activityInput.value;

        button.textContent = "Save";

        const cancelButton = document.getElementById(`cancel-button-${id}`);
        cancelButton.hidden = false;

        const deleteButton = document.getElementById(`delete-button-${id}`);
        deleteButton.hidden = true;

        const textDisplay = row.querySelector('.text-display');
        textDisplay.hidden = true;
    } else {
        document.getElementById(`cancel-button-${id}`).hidden = true;
        button.closest("form").submit();

        return;
    }

    const milesDisplay = row.querySelector('.miles-display');
    const runDateDisplay = row.querySelector('.run-date-display');
    const activityDisplay = row.querySelector('.activity-display');

    milesDisplay.hidden = true;
    runDateDisplay.hidden = true;
    activityDisplay.hidden = true;

    milesInput.hidden = false;
    runDateInput.hidden = false;
    activityInput.hidden = false;
}

function cancelEditRun(id) {
    const row = document.getElementById(`run-${id}`);

    const milesInput = row.querySelector('input[name="miles"]');
    const runDateInput = row.querySelector('input[name="run_date"]');
    const activityInput = row.querySelector('select[name="activity"]');
    const textDisplay = row.querySelector('.text-display');
    textDisplay.hidden = false;

    milesInput.value = row.dataset.originalMiles;
    runDateInput.value = row.dataset.originalDate;
    activityInput.value = row.dataset.originalActivity;

    const button = document.getElementById(`edit-button-${id}`);
    button.textContent = "Edit";
    document.getElementById(`cancel-button-${id}`).hidden = true;

    const deleteButton = document.getElementById(`delete-button-${id}`);
    deleteButton.hidden = false;

    row.querySelector('.miles-display').hidden = false;
    row.querySelector('.run-date-display').hidden = false;
    row.querySelector('.activity-display').hidden = false;

    milesInput.hidden = true;
    runDateInput.hidden = true;
    activityInput.hidden = true;
}

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

confirmDeleteRun.forEach(form => {
    form.addEventListener("submit", function(event) {

        if (!confirm("Are you sure you want to delete this entry?")) {
            event.preventDefault();
        }
    })
})


confirmDeletePhoto.forEach(form => {
    form.addEventListener("submit", function(event) {

        if (!confirm("Are you sure you want to delete this entry?")) {
            event.preventDefault();
        }
    })
})

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