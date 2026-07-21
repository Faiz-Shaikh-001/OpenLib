function openNav() {
    document.getElementById("mySidenav").style.width = "250px";
}

function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
}

// Define an object to store currentIndex for different containers
const currentIndex = {};

function scrollBooks(containerId, direction) {
    const container = document.getElementById(containerId);

    function showSlide(index, container) {
        const bookWrapper = container.querySelector('.book-wrapper');
        bookWrapper.style.transform = `translateX(-${index * 220}px`; // Adjust 220 to match your book width
    }

    if (container) {
        // Initialize currentIndex for the specific container if it doesn't exist
        if (!currentIndex[containerId]) {
            currentIndex[containerId] = 0;
        }

        if (direction === "next") {
            currentIndex[containerId] = Math.min(currentIndex[containerId] + 1, container.querySelectorAll('.book').length - 3); // Adjust -3 to match the number of visible books
            showSlide(currentIndex[containerId], container);
        } else if (direction === "prev") {
            currentIndex[containerId] = Math.max(currentIndex[containerId] - 1, 0);
            showSlide(currentIndex[containerId], container);
        }

        // Add the smooth-scroll class to enable the transition effect
        container.classList.add("smooth-scroll");

        // After the scroll animation is complete (adjust the timeout duration as needed)
        setTimeout(() => {
            container.classList.remove("smooth-scroll");
        }, 300); // 300ms is the duration of your transition in the CSS
    }
}
