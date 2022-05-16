const filterbox = document.querySelectorAll('.card-places');

document.querySelector('.type').addEventListener('click', event => {

    if (event.target.tagName !== 'SPAN') return false;

    let filterClass = event.target.dataset['f'];

    filterbox.forEach(elem => {
        console.log(filterClass)
        console.log(elem.classList)
        elem.classList.remove('hide');

        var nodes = document.getElementById('type').getElementsByTagName("span");
        for(var i=0; i<nodes.length; i++) {
            nodes[i].classList.remove('bg-success');
            nodes[i].classList.add('bg-dark');
        }

        if (!elem.classList.contains(filterClass) && filterClass !== 'all') {
            elem.classList.add('hide');
        }
        event.target.classList.remove('bg-dark');
        event.target.classList.add('bg-success');
    });
});

document.querySelector('.city').addEventListener('click', event => {
    if (event.target.tagName !== 'SPAN') return false;

    let filterClass = event.target.dataset['f'];

    filterbox.forEach(elem => {
        elem.classList.remove('hidecity');

        var nodes = document.getElementById('city').getElementsByTagName("span");
        for(var i=0; i<nodes.length; i++) {
            nodes[i].classList.remove('bg-success');
            nodes[i].classList.add('bg-dark');
        }

        if (!elem.classList.contains(filterClass) && filterClass !== 'All cities') {
            elem.classList.add('hidecity');
        }
        event.target.classList.remove('bg-dark');
        event.target.classList.add('bg-success');
    });
});