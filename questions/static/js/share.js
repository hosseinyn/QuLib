const share_button = document.getElementById("shareBtn")

const shareData = {
  title: share_button.dataset.title,
  text: share_button.dataset.description,
  url: window.location.href,
};

share_button.addEventListener("click", async () => {
  await navigator.share(shareData)
});