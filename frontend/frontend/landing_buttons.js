// Simple navigation to the user portal
document.getElementById("btn-register").onclick =
document.getElementById("btn-login").onclick =
document.getElementById("try-app").onclick =
document.getElementById("get-started").onclick = () => {
  window.location.href = "user.html";
};

document.getElementById("convert-api").onclick = () => alert("API coming soon.");
document.getElementById("ai-helper").onclick = () => alert("AI helper coming soon.");
