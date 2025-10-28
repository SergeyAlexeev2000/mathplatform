const BASE = "http://127.0.0.1:8000";
const els = (sel) => document.querySelector(sel);
const show = (id, on=true) => els(id).classList[on ? "remove" : "add"]("hidden");

const drawer = els("#drawer");
els("#menu").onclick = () => drawer.classList.toggle("show");

const tokenStore = {
  get() { return localStorage.getItem("access_token") || sessionStorage.getItem("access_token"); },
  set(tok, remember) {
    localStorage.removeItem("access_token"); sessionStorage.removeItem("access_token");
    (remember ? localStorage : sessionStorage).setItem("access_token", tok);
  },
  clear() { localStorage.removeItem("access_token"); sessionStorage.removeItem("access_token"); }
};

async function api(path, {method="GET", body, auth=true}={}) {
  const headers = { "Content-Type":"application/json" };
  if (auth) {
    const tok = tokenStore.get();
    if (tok) headers["Authorization"] = "Bearer " + tok;
  }
  const res = await fetch(BASE + path, { method, headers, body: body ? JSON.stringify(body) : undefined });
  if (!res.ok) throw new Error((await res.text()) || res.statusText);
  return res.json();
}

async function register() {
  els("#reg-status").textContent = "Registering...";
  try {
    const email = els("#reg-email").value.trim();
    const username = els("#reg-username").value.trim();
    const password = els("#reg-password").value;
    await api("/auth/register", { method:"POST", body: { email, username, password }, auth:false });
    els("#reg-status").textContent = "Verification passed successfully ✓";
    show("#post-register", true);
  } catch (e) {
    els("#reg-status").textContent = parseError(e);
  }
}

async function login() {
  els("#login-status").textContent = "Signing in...";
  try {
    const login = els("#login-id").value.trim();
    const password = els("#login-password").value;
    const remember = els("#remember").checked;
    const data = await api("/auth/login", { method:"POST", body: { login, password, remember }, auth:false });
    tokenStore.set(data.access_token, remember);
    els("#login-status").textContent = "Login OK ✓";
    await loadAccount();
  } catch (e) {
    els("#login-status").textContent = parseError(e);
  }
}

function parseError(err) {
  const t = String(err.message || err);
  if (t.includes("email_exists")) return "This email already exists.";
  if (t.includes("username_exists")) return "This username already exists.";
  if (t.includes("invalid credentials")) return "Invalid credentials.";
  return t;
}

async function loadAccount() {
  try {
    const me = await api("/auth/me");
    // header greeter
    els("#hello-name").textContent = me.username || me.email || "user";
    els("#hello-status").textContent = me.is_verified ? "online" : "pending";

    // account card
    els("#user-name").textContent = me.username || me.email;
    show("#auth-card", false);
    show("#account", true);

    // demo lists
    renderList("#recent-list", [
      "Differential Geometry — Week 1",
      "Functional Analysis: Hahn–Banach",
      "Category Theory: Yoneda Lemma"
    ]);
    renderList("#suggest-list", [
      "Geometric Measure Theory — Intro",
      "Automated Theorem Proving — Basics",
      "Distribution Theory — Schwartz spaces"
    ]);
  } catch (e) {
    // if token invalid — show auth card
    tokenStore.clear();
    show("#account", false);
    show("#auth-card", true);
  }
}

function renderList(sel, items) {
  const ul = els(sel);
  ul.innerHTML = "";
  for (const it of items) {
    const li = document.createElement("li");
    li.textContent = it;
    ul.appendChild(li);
  }
}

// Buttons
els("#btn-register").onclick = register;
els("#confirm").onclick = () => {
  // purely visual in this mock; backend already accepted registration
  alert("Confirmed!");
};
els("#btn-login").onclick = login;
els("#logout").onclick = () => { tokenStore.clear(); location.reload(); };

// Auto-login if token exists
if (tokenStore.get()) loadAccount();
