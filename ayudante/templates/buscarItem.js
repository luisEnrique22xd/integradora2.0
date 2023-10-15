document.addEventListener("DOMContentLoaded", function() {
    const searchButton = document.getElementById("search-button");
    const searchInput = document.getElementById("search-input");

    searchButton.addEventListener("click", function() {
        const searchTerm = searchInput.value.trim().toLowerCase();

        // Realizar la solicitud GET al servidor Flask con el término de búsqueda
        fetch('/buscarItem?searchTerm=' + searchTerm)
        .then(response => response.json())
        .then(data => {
            // Aquí recibes la respuesta del servidor Flask con los resultados de búsqueda
            // Puedes mostrarlos en la página o hacer cualquier otra operación con ellos.
            console.log(data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});
