function openNav() {
    document.getElementById("mySidenav").style.width = "250px";
}

function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
}

// JavaScript code for toggling visibility
document.addEventListener('DOMContentLoaded', () => {
    const mainSection = document.getElementById('main');
    const addBookSection = document.getElementById('add-book');
    const manageUserSection = document.getElementById('manage-user-container');
    const issueBookSection = document.getElementById('issue-book-container');
    const returnBookSection = document.getElementById('return-book-container');
    const viewRecordSection = document.getElementById('view-record-container');
    
    const dashboardLink = document.querySelector('.sidenav a[href="#main"]');
    const addBookLink = document.querySelector('.sidenav a[href="#add-book"]');
    const manageUserLink =  document.querySelector('.sidenav a[href="#manage-user"]');
    const issueBookLink =  document.querySelector('.sidenav a[href="#issue-book"]');
    const returnBookLink =  document.querySelector('.sidenav a[href="#return-book"]');
    const viewRecordLink =  document.querySelector('.sidenav a[href="#view-records"]');
    
    // Function to open the "Dashboard" section
    function openMainSection() {
        mainSection.style.display = 'block';
        addBookSection.style.display = 'none';
        manageUserSection.style.display = 'none';
        issueBookSection.style.display = 'none';
        returnBookSection.style.display = 'none';
        viewRecordSection.style.display = 'none';
    }
    // Function to open the "Add Book" section
    function openAddBookSection() {
        addBookSection.style.display = 'block';
        mainSection.style.display = 'none';
        manageUserSection.style.display = 'none';
        issueBookSection.style.display = 'none';
        returnBookSection.style.display = 'none';
        viewRecordSection.style.display = 'none';
    }
    // Function to open the "Manage User" section
    function openManageUser() {
        manageUserSection.style.display = 'block';
        mainSection.style.display = 'none';
        addBookSection.style.display = 'none';
        issueBookSection.style.display = 'none';
        returnBookSection.style.display = 'none';
        viewRecordSection.style.display = 'none';
    }

    function openIssueBookSection() {
        issueBookSection.style.display = 'block';
        mainSection.style.display = 'none';
        addBookSection.style.display = 'none';
        manageUserSection.style.display = 'none';
        returnBookSection.style.display = 'none';
        viewRecordSection.style.display = 'none';
    }

    function openReturnBookSection() {
        returnBookSection.style.display = 'block';
        mainSection.style.display = 'none';
        addBookSection.style.display = 'none';
        manageUserSection.style.display = 'none';
        issueBookSection.style.display = 'none';
        viewRecordSection.style.display = 'none';
    }

    function openViewRecordSection() {
        viewRecordSection.style.display = 'block';
        mainSection.style.display = 'none';
        addBookSection.style.display = 'none';
        manageUserSection.style.display = 'none';
        issueBookSection.style.display = 'none';
        returnBookSection.style.display = 'none';
    }

    
    // Event listener for the "Add Book" link
    addBookLink.addEventListener('click', openAddBookSection);
    dashboardLink.addEventListener('click', openMainSection);
    manageUserLink.addEventListener('click', openManageUser);
    issueBookLink.addEventListener('click', openIssueBookSection);
    returnBookLink.addEventListener('click', openReturnBookSection);
    viewRecordLink.addEventListener('click', openViewRecordSection);

});


// search element in table
const searchInput = document.getElementById('search');
const tableRows = document.querySelectorAll('#book-table tbody tr');

searchInput.addEventListener('input', function () {
    const searchText = searchInput.value.toLowerCase();
    let scrolled = false;

    tableRows.forEach(row => {
        const title = row.cells[1].textContent.toLowerCase();
        const author = row.cells[2].textContent.toLowerCase();

        if (searchText === '' | title.includes(searchText) || author.includes(searchText)) {
            row.classList.add('highlight');

            if (!scrolled) {
                // Scroll to the first highlighted row
                const tableContainer = document.querySelector('.table-container');
                tableContainer.scrollTop = row.offsetTop - tableContainer.offsetTop;
                scrolled = true;
            }

        } else {
            row.classList.remove('highlight');
        }

        // Remove the highlight immediately if the search input is empty
        if (searchText === '') {
            tableRows.forEach(row => {
                row.classList.remove('highlight');
            });
        }
    });
});