/* Project specific Javascript goes here. */
const messages = document.querySelectorAll(".django-message");

messages.forEach(m => {
  const close_btn = m.querySelector(".btn-close");
  close_btn.addEventListener("click", e => {
    m.remove();
  });
});
