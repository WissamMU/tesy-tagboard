(function () { // Self invoking function to avoid variable clashing
  let root = document.querySelector(".add-tagset-container");
  let search_input = root.querySelector("input[type='search']")

  function get_search_results() {
    return root.querySelector(".result-container ul");
  }

  htmx.on(root.querySelector(".result-container"), "htmx:afterSettle", (e) => {
    let tagset = htmx.find(".tagset");
    let search_results = get_search_results();
    if (search_results) {
      Array.from(search_results.children).forEach(autocomplete_item => {
        htmx.on(autocomplete_item, "mousedown", function(e) {
          let tag_id = autocomplete_item.dataset['id'];
          let tag_name = autocomplete_item.dataset['name'];

          let tag_div = document.createElement("div");
          tag_div.classList.add("rounded-md", "bg-secondary", "text-secondary-content", "h-8", "px-2", "py-1");
          tag_div.textContent = tag_name;

          let tag_input = document.createElement("input");
          tag_input.setAttribute("id", `tag-${tag_id}`);
          tag_input.setAttribute("type", "hidden");
          tag_input.setAttribute("name", "tagset");
          tag_input.setAttribute("value", tag_id);

          tag_div.appendChild(tag_input);
          tagset.appendChild(tag_div);
        });
      });
    }
  });
})();
