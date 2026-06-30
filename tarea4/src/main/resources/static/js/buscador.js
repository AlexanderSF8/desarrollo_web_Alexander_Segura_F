let inputSearch = document.getElementById("search-input");
let matchSearch = document.getElementById("search-list");

// Función mágica para destacar el texto
const destacarTexto = (textoBase, palabraBuscada) => {
    if (!textoBase || !palabraBuscada) return textoBase;
    // Crea una expresión regular que ignora mayúsculas/minúsculas
    const regex = new RegExp(`(${palabraBuscada})`, 'gi');
    return textoBase.replace(regex, '<mark>$1</mark>'); 
};

let populateMatchList = (matchList, keyword) => {
    matchSearch.innerHTML = ""; // Limpiamos resultados anteriores

    if (matchList.length === 0) {
        matchSearch.innerHTML = "<p>No se encontraron actividades.</p>";
        return;
    }

    matchList.forEach(act => {
        let div = document.createElement("div");
        div.className = "resultado-actividad"; 
        
        let nombreDestacado = destacarTexto(act.miembroNombre, keyword);
        let descripcionDestacada = destacarTexto(act.descripcion, keyword);
        let comunaDestacada = destacarTexto(act.comuna, keyword);

        div.innerHTML = `
            <div class="info-actividad">
                <p><strong>Miembro:</strong> ${nombreDestacado}</p>
                <p><strong>Día:</strong> ${act.dia} | <strong>Tipo:</strong> ${act.tipo}</p>
                <p><strong>Comuna:</strong> ${comunaDestacada}</p>
                <p><strong>Descripción:</strong> ${descripcionDestacada}</p>
            </div>
            <div class="evaluacion-box">
                <span>Nota Promedio: <strong>${act.nota}</strong></span>
                <input type="number" id="nota-input-${act.id}" min="1" max="7" placeholder="1-7">
                <button onclick="enviarNota(${act.id})">Evaluar</button>
            </div>
        
        `;
        matchSearch.appendChild(div);
    });
};

// Evento que se dispara cada vez que se teclea
inputSearch.addEventListener("input", (event) => {
    let keyword = event.target.value.trim();

    // Buscar solo a partir de 3 caracteres
    if (keyword.length >= 3) {
        fetch(`http://localhost:8080/api/actividades/${keyword}`)
            .then(response => response.json())
            .then(ajaxResponse => {
                populateMatchList(ajaxResponse.data, keyword);
            })
            .catch(error => console.error("Error en la búsqueda:", error));
    } else {
        matchSearch.innerHTML = ""; // Limpiamos si hay menos de 3 letras
    }
});

// Función asíncrona para guardar la nota
const enviarNota = (id) => {
    let valorNota = document.getElementById(`nota-input-${id}`).value;
    
    if (valorNota >= 1 && valorNota <= 7) {
        fetch(`http://localhost:8080/api/actividades/${id}/evaluar`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ nota: parseInt(valorNota) })
        })
        .then(response => response.json())
        .then(data => {
            if(data.status === "ok") {
    
                inputSearch.dispatchEvent(new Event('input')); 
            }
        });
    } else {
        alert("La nota debe ser un número entre 1 y 7.");
    }
};