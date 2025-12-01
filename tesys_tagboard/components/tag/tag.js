(function () { // Self invoking function to avoid variable clashing
  let tagAction = (action, tag_id) => {
    return new CustomEvent("tagAction", {
      bubbles: true,
      detail: { action: action, tag_id: tag_id}
    });
  }

  document.querySelectorAll(".tag-container").forEach(tag => {
    tag.addEventListener("tagAction", e => {
      if (e.detail.action == "remove") {
        tag.remove();
      }
    });
  });

  document.querySelectorAll(".tag-form .tag-actions button").forEach(btn => {
    htmx.on(btn, "click", (e) => {
      const action = btn.dataset["action"];
      const tag_id = btn.datset["tag_id"];
      btn.dispatchEvent(tagAction(action, tag_id));
    });
  });
})();
