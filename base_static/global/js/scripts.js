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


document.addEventListener("DOMContentLoaded", function() {
  const tooltipImage = document.getElementById('tooltip-image');
  const tooltipImageSrc = document.getElementById('tooltip-image-src');

  document.querySelectorAll('.product-name').forEach(function(element) {
      element.addEventListener('mouseover', function(event) {
          const imageUrl = event.target.getAttribute('data-image-url');
          if (imageUrl) {
              tooltipImageSrc.src = imageUrl;
              tooltipImage.style.display = 'block';
          }
      });

      element.addEventListener('mousemove', function(event) {
          tooltipImage.style.top = (event.pageY + 10) + 'px';
          tooltipImage.style.left = (event.pageX + 10) + 'px';
      });

      element.addEventListener('mouseout', function() {
          tooltipImage.style.display = 'none';
      });
  });
});
