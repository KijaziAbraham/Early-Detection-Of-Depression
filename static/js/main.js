
(function() {
  "use strict";

  /**
   * Easy selector helper function
   */
  const select = (el, all = false) => {
    el = el.trim()
    if (all) {
      return [...document.querySelectorAll(el)]
    } else {
      return document.querySelector(el)
    }
  }

  /**
   * Easy event listener function
   */
  const on = (type, el, listener, all = false) => {
    let selectEl = select(el, all)
    if (selectEl) {
      if (all) {
        selectEl.forEach(e => e.addEventListener(type, listener))
      } else {
        selectEl.addEventListener(type, listener)
      }
    }
  }

  /**
   * Easy on scroll event listener 
   */
  const onscroll = (el, listener) => {
    el.addEventListener('scroll', listener)
  }

  /**
   * Toggle .header-scrolled class to #header when page is scrolled
   */
  let selectHeader = select('#header')
  if (selectHeader) {
    const headerScrolled = () => {
      if (window.scrollY > 100) {
        selectHeader.classList.add('header-scrolled')
      } else {
        selectHeader.classList.remove('header-scrolled')
      }
    }
    window.addEventListener('load', headerScrolled)
    onscroll(document, headerScrolled)
  }

  /**
   * Mobile nav toggle
   */
  on('click', '.mobile-nav-toggle', function(e) {
    select('#navbar').classList.toggle('navbar-mobile')
    this.classList.toggle('bi-list')
    this.classList.toggle('bi-x')
  })

  /**
   * Back to top button
   */
  let backtotop = select('.back-to-top')
  if (backtotop) {
    const toggleBacktotop = () => {
      if (window.scrollY > 100) {
        backtotop.classList.add('active')
      } else {
        backtotop.classList.remove('active')
      }
    }
    window.addEventListener('load', toggleBacktotop)
    onscroll(document, toggleBacktotop)
  }

  /**
   * Mobile nav dropdowns activate
   */
  on('click', '.navbar .dropdown > a', function(e) {
    if (select('#navbar').classList.contains('navbar-mobile')) {
      e.preventDefault()
      this.nextElementSibling.classList.toggle('dropdown-active')
    }
  }, true)

  /**
   * Testimonials slider
   */
  new Swiper('.testimonials-slider', {
    speed: 600,
    loop: true,
    autoplay: {
      delay: 5000,
      disableOnInteraction: false
    },
    slidesPerView: 'auto',
    pagination: {
      el: '.swiper-pagination',
      type: 'bullets',
      clickable: true
    }
  });

  /**
   * Animation on scroll
   */
  window.addEventListener('load', () => {
    AOS.init({
      duration: 1000,
      easing: 'ease-in-out',
      once: true,
      mirror: false
    })
  });

})()
document.addEventListener("DOMContentLoaded", function() {
  const registrationForm = document.querySelector("#registration-form");
  const loginForm = document.querySelector("#login-form");
  const alertContainer = document.getElementById("alert-container");

  registrationForm.addEventListener("submit", function(event) {
      event.preventDefault(); // Prevent the default form submission
      // Simulate error response
      const data = {
          "success": false,
          "errors": ["This field is required.", "Another field is required."]
      };
      displayAlert(data);
  });

  loginForm.addEventListener("submit", function(event) {
      event.preventDefault(); // Prevent the default form submission
      // Simulate error response
      const data = {
          "success": false,
          "errors": ["Invalid username.", "Incorrect password."]
      };
      displayAlert(data);
  });

  function displayAlert(data) {
      if (!data.success && data.errors.length > 0) {
          const errorMessage = data.errors.join("\n");
          alertContainer.innerHTML = errorMessage;
          alertContainer.style.display = "block";
          // Automatically hide the alert after a delay (optional)
          setTimeout(() => {
              alertContainer.style.display = "none";
          }, 5000); // Adjust the delay as needed
      }
  }
});



$(document).ready(function() {
  // Add focus class when input is focused
  $('input, select').focus(function(event) {
      $(this).closest('.float-label-field').addClass('float').addClass('focus');
  });

  // Remove focus class when input is blurred
  $('input, select').blur(function() {
      $(this).closest('.float-label-field').removeClass('focus');
      if (!$(this).val()) {
          $(this).closest('.float-label-field').removeClass('float');
      }
  });
});
