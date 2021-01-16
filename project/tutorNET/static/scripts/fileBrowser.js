/** @type {HTMLInputElement} */
const photoInput = document.getElementById("profile-photo");

/** @type {HTMLLabelElement} */
const photoLabel = document.getElementById("photo-label");

photoInput.addEventListener("change", function (e) {
	let value = e.target.value.split("\\");
	console.log(value);
	photoLabel.textContent = value[value.length - 1];
});
