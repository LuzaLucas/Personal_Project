(() => {
    console.log("Logout script loaded");
    const logoutLink = document.querySelector('.users-logout-link');
    const formLogout = document.querySelector('.form-logout');

    if (logoutLink && formLogout) {
        logoutLink.addEventListener('click', (e) => {
            e.preventDefault();
            formLogout.submit();
        });
    } else {
        console.error("Logout link or form not found");
    }
})();
