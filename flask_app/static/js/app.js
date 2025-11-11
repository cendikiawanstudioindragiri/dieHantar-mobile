console.log('Flask app JS loaded');

// Auto-dismiss non-error alerts after 5 seconds
window.addEventListener('load', () => {
	const alerts = document.querySelectorAll('.alert');
	alerts.forEach((el) => {
		if (el.classList.contains('alert-danger')) return; // keep errors until closed
		setTimeout(() => {
			el.setAttribute('closing', '');
			setTimeout(() => el.remove(), 200);
		}, 5000);
	});
});
