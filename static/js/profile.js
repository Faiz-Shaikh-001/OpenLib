// Load user data from a hypothetical API
const userData = {
    name: "John Doe",
    email: "john.doe@example.com",
    phone: "123-456-7890",
    location: "New York, USA",
};

// Function to populate the form with user data
function populateForm(userData) {
    document.getElementById("name").value = userData.name;
    document.getElementById("email").value = userData.email;
    document.getElementById("phone").value = userData.phone;
    document.getElementById("location").value = userData.location;
}

// Function to update the user information in the user info section
function updateUserInfo(userData) {
    document.getElementById("userName").textContent = userData.name;
    document.getElementById("userEmail").textContent = userData.email;
    document.getElementById("userPhone").textContent = userData.phone;
    document.getElementById("userLocation").textContent = userData.location;
}

// Populate the form with user data
populateForm(userData);

// Add an event listener to the form for form submission
document.getElementById("profileForm").addEventListener("submit", function (event) {
    event.preventDefault(); // Prevent the default form submission

    // Get user input from the form
    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const phone = document.getElementById("phone").value;
    const location = document.getElementById("location").value;

    // Update the user information in the user info section
    const updatedUserData = {
        name,
        email,
        phone,
        location,
    };
    updateUserInfo(updatedUserData);

    // You can also send the updated information to a server for storage here

    alert("Profile updated successfully!");
});

// profile pic update
document.addEventListener('DOMContentLoaded', function () {
    var profilePic = document.querySelector('.profile-pic');
    var fileUpload = document.querySelector('.file-upload');
    var uploadButton = document.querySelector('.upload-button');

    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();

            reader.onload = function (e) {
                profilePic.setAttribute('src', e.target.result); // Set the 'src' attribute
            };

            reader.readAsDataURL(input.files[0]);
        }
    }

    fileUpload.addEventListener('change', function () {
        readURL(this);
    });

    uploadButton.addEventListener('click', function () {
        fileUpload.click();
    });
});
