/** @type {HTMLDivElement} */
const rememberDiv = document.querySelector(".remember");
/** @type {HTMLDivElement} */
const forgetDiv = document.querySelector(".forget");
const form = document.querySelector("form");
/** @type {HTMLInputElement} */
const nameInput = document.querySelector("#input-name");
/** @type {HTMLInputElement} */
const submitBtn = document.querySelector("#submit-name");
/** @type {HTMLInputElement} */
const forgetBtn = document.querySelector("#forget-name");

/** @type {HTMLParagraphElement} */
const greeting = document.querySelector(".greeting");

form.addEventListener("submit", (e) => {
	e.preventDefault();
});

submitBtn.addEventListener("click", () => {
	localStorage.setItem("name", nameInput.value);
	nameDisplayCheck();
});

forgetBtn.addEventListener("click", () => {
	localStorage.removeItem("name");
	nameDisplayCheck();
});

function nameDisplayCheck() {
	// check whether the 'name' data item is stored in web Storage
	if (localStorage.getItem("name")) {
		// If it is, display personalized greeting
		let name = localStorage.getItem("name");
		greeting.textContent = "Welcome, " + name;
		forgetDiv.style.display = "flex";
		rememberDiv.style.display = "none";
	} else {
		greeting.textContent = "Welcome";
		forgetDiv.style.display = "none";
		rememberDiv.style.display = "flex";
	}
}

window.onload = nameDisplayCheck;
