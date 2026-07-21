document.addEventListener("DOMContentLoaded", () => {
  const profileButton = document.querySelector(
    'button[type="button"] img',
  )?.parentElement;

  const profileMenu = document.getElementById("profileMenu");

  if (!profileButton || !profileMenu) return;

  profileButton.addEventListener("click", (e) => {
    e.stopPropagation();
    profileMenu.classList.toggle("hidden");
  });

  document.addEventListener("click", () => {
    profileMenu.classList.add("hidden");
  });
});

const mobileBtn = document.getElementById("mobileBtn");
const mobileNav = document.getElementById("mobileNav");
const logo = document.getElementById("logo");

mobileBtn.addEventListener("click", () => {
  mobileNav.classList.toggle("hidden");
  logo.classList.toggle("hidden")
});

const joinNews = (e) => {
    e.preventDefault();

    const email_address = document.getElementById("NewsEmail").value;

    fetch("/news/api/subscribers", {
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        method: "POST",
        body: JSON.stringify({ email: email_address })
    })
    .then(response => {
        if (response.ok) {
            alert("ممنون! پشیمون نمیشی");
        }
    })
}