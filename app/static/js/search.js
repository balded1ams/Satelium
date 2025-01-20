const searchInput = document.getElementById('searchInput');
const resultsList = document.getElementById('results');



searchInput.addEventListener('input', () => {
    const query = searchInput.value.trim();
    if (query.length === 0) {
        resultsList.innerHTML = '';
        return;
    }

    fetch(`/api/search?query=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(results => {
            resultsList.innerHTML = '';
            results.forEach(result => {
                const li = document.createElement('li');
                li.textContent = result.name;
                li.addEventListener('click', () => {
                    var trackedSats = JSON.parse(localStorage.getItem("trackedSats"))
                    if (trackedSats === null){
                        trackedSats = []
                    }
                    var satIdx = trackedSats.indexOf(result.id)
                    if (satIdx > -1)
                        trackedSats.splice(trackedSats.indexOf(result.id), 1);
                    else
                        trackedSats.push(result.id)
                    localStorage.setItem("trackedSats", JSON.stringify(trackedSats))
                    initMarkers()
                    console.log('Selected satellite:', result);
                });
                resultsList.appendChild(li);
            });
        });
});