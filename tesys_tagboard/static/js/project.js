/* Project specific Javascript goes here. */
document.querySelectorAll('button.btn:not([type="submit"])').forEach(btn => {
  btn.addEventListener("click", (e) => {
    // Stop regular buttons from clicking "through" elements
    e.stopPropagation();
    e.preventDefault();
  });
});
