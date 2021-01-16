// @ts-nocheck

/** @type {HTMLButtonElement} */
const addBtn = document.querySelector("#add-time");

/** @type {HTMLButtonElement} */
const removeBtn = document.querySelector("#remove-time");

/** @type {HTMLDivElement} */
const timeField = document.querySelector("#time-table");

/** @type {HTMLDivElement} */
const form = document.getElementById("add-subject-form");

/** @type {HTMLButtonElement} */
const submitBtn = document.getElementById("submit-btn");

window.onload = function () {
	removeBtn.setAttribute("disabled", "");
};
let c = 1;

addBtn.addEventListener("click", function () {
	const timeField = document.querySelector(".time-table");

	const newField = timeField.cloneNode(true);

	newField.querySelector("#weekday-label").setAttribute("for", "weekday_" + c);
	newField.querySelector("#weekday").setAttribute("id", "weekday_" + c);

	newField.querySelector("#from-label").setAttribute("for", "time-from_" + c);
	newField.querySelector("#time-from").setAttribute("id", "time-from_" + c);

	newField.querySelector("#to-label").setAttribute("for", "time-to_" + c);
	newField.querySelector("#time-to").setAttribute("id", "time-to_" + c);

	c = c + 1;
	const inputs = newField.querySelectorAll("input");

	for (let i = 0, len = inputs.length; i < len; i++) {
		inputs[i].value = "";
	}
	// limit schedules to 5
	if (c === 5) {
		addBtn.setAttribute("disabled", "");
	}
	if (c > 1) {
		removeBtn.removeAttribute("disabled");
	}
	form.removeChild(submitBtn);
	form.appendChild(newField);
	form.appendChild(submitBtn);
});

removeBtn.addEventListener("click", function () {
	const timeFields = document.querySelectorAll(".time-table");
	let len = timeFields.length - 1;
	// if a schedule is removed, enable addBtn again
	c = c - 1;
	if (c !== 5) {
		addBtn.removeAttribute("disabled");
	}
	if (c === 1) {
		removeBtn.setAttribute("disabled", "");
	}

	form.removeChild(timeFields.item(len));
});
