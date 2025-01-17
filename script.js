const map = L.map('map').setView([48.8566, 2.3522], 13);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

//barre de recherche
const searchBar = document.querySelector('.search-bar');
const searchInput = document.getElementById('search-input');

function activateSearchBar() {
    searchBar.classList.add('active');
    searchInput.focus(); // Place automatiquement le curseur dans la barre
}
function deactivateSearchBar() {
    searchBar.classList.remove('active');
}

searchInput.addEventListener('click', activateSearchBar);

document.addEventListener('click', (event) => {
    if (!searchBar.contains(event.target)) {
        deactivateSearchBar();
    }
})

document.addEventListener('keydown', (event) => {
    if (event.ctrlKey && event.key.toLowerCase() === 'k') {
        event.preventDefault(); // Empêche le comportement par défaut
        if (searchBar.classList.contains('active')) {
            deactivateSearchBar();
        } else {
            activateSearchBar();
        }
    }
});