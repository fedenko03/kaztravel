function submit(evt) {
	evt.preventDefault();
}

function filter(evt) {
	evt.preventDefault();
	let input = document.querySelector('#site-search');
	let inputValue = input.value.toUpperCase();
	let cards = document.querySelectorAll('.title-place');

	cards.forEach(
		function getMatch(info) {
			let heading = info.querySelector('h4');
			let headingContent = heading.innerHTML.toUpperCase();

			if (headingContent.includes(inputValue)) {
				info.classList.remove('hide-search');
			}
			else {
				info.classList.add('hide-search');
			}
		}
	)
}

function autoReset() {
	let input = document.querySelector('#site-search');
	let cards = document.querySelectorAll('.title-place');

	cards.forEach(
		function getMatch(info) {
			if (input.value == null, input.value == "") {
				info.classList.remove('hide-search');
				info.classList.remove('hide-search');
			}
			else {
				return;
			}
		}
	)
}

let form = document.querySelector('.search-form');

form.addEventListener('keyup', filter);

form.addEventListener('submit', submit);