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


function my_scope() {
    const forms = document.querySelectorAll('.form-delete');
    
    for (const form of forms) {
      form.addEventListener('submit', function (e) {
        e.preventDefault();
  
        const confirmed = confirm('Are you sure?');
  
        if (confirmed) {
          form.submit();
        }
      });
    }
  }
  my_scope();