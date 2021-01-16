const path = document.location.pathname;

const nav = document.querySelector(`a[href="${path}"]`);

window.onload = () => {
	nav.setAttribute("class", "nav-link active");
};

// JQuery for showing toasts
$(".toast").toast("show");
