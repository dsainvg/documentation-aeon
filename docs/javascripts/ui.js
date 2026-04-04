document.addEventListener("DOMContentLoaded", () => {
  const copyText = async (text) => {
    if (navigator.clipboard && window.isSecureContext) {
      await navigator.clipboard.writeText(text);
      return;
    }

    const helper = document.createElement("textarea");
    helper.value = text;
    helper.setAttribute("readonly", "");
    helper.style.position = "absolute";
    helper.style.left = "-9999px";
    document.body.appendChild(helper);
    helper.select();
    document.execCommand("copy");
    document.body.removeChild(helper);
  };

  document.querySelectorAll("pre > code").forEach((codeBlock) => {
    const pre = codeBlock.parentElement;
    if (!pre || pre.querySelector(".aeon-copy-button")) {
      return;
    }

    pre.classList.add("aeon-codeblock");

    const button = document.createElement("button");
    button.type = "button";
    button.className = "aeon-copy-button";
    button.innerHTML = '<i class="fa-regular fa-copy" aria-hidden="true"></i>';
    button.setAttribute("aria-label", "Copy code to clipboard");
    button.title = "Copy code";

    button.addEventListener("click", async () => {
      const original = button.innerHTML;
      try {
        await copyText(codeBlock.innerText.trimEnd());
        button.innerHTML = '<i class="fa-solid fa-check" aria-hidden="true"></i>';
        button.classList.add("is-copied");
      } catch {
        button.innerHTML = '<i class="fa-solid fa-xmark" aria-hidden="true"></i>';
        button.classList.add("is-copied");
      }

      window.setTimeout(() => {
        button.innerHTML = original;
        button.classList.remove("is-copied");
      }, 1400);
    });

    pre.appendChild(button);
  });

  document.querySelectorAll("table").forEach((table) => {
    if (table.parentElement && table.parentElement.classList.contains("aeon-table-wrap")) {
      return;
    }

    const wrapper = document.createElement("div");
    wrapper.className = "aeon-table-wrap";
    table.parentNode.insertBefore(wrapper, table);
    wrapper.appendChild(table);
    table.classList.add("aeon-table");
  });
});
