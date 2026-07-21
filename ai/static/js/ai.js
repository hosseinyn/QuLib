function toggleSidebar() {
  const sidebar = document.getElementById("sidebar");
  const overlay = document.getElementById("sidebar-overlay");

  sidebar.classList.toggle("translate-x-full");
  overlay.classList.toggle("hidden");
}

document.addEventListener("DOMContentLoaded", function () {
  const textarea = document.getElementById("message-input");

  function autoResize() {
    textarea.style.height = "auto";
    textarea.style.height = Math.min(textarea.scrollHeight, 180) + "px";
  }

  textarea.addEventListener("input", autoResize);
  textarea.addEventListener("keydown", function (e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });
});
