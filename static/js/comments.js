document.addEventListener('DOMContentLoaded', () => {
    
    // Catch DOM elements
    const actividadId = document.getElementById('actividad_id').value;
    const btnToggle = document.getElementById('btn-toggle-form');
    const formContainer = document.getElementById('comment-form-container');
    const btnCancel = document.getElementById('btn-cancel-comment');
    const commentsList = document.getElementById('comments-list');

    // ==========================================
    // VISUAL LOGIC: HIDE/SHOW FORM
    // ==========================================
    
    // Al presionar el botón "+" (Naranjo)
    btnToggle.addEventListener('click', () => {
        formContainer.classList.remove('d-none'); 
        btnToggle.classList.add('d-none');       
    });

    // Al presionar el botón "Cancelar" (Gris)
    btnCancel.addEventListener('click', () => {
        formContainer.classList.add('d-none');    
        btnToggle.classList.remove('d-none');   
    });


    // ==========================================
    // ASYNC LOGIC: LOAD COMMENTS (FETCH)
    // ==========================================
    
    const loadComments = () => {
        fetch(`/api/comments/${actividadId}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Error al conectar con la API');
                }
                return response.json();
            })
            .then(data => {
                // if not comments, show a friendly message 
                if (data.length === 0) {
                    commentsList.innerHTML = `
                        <div class="alert alert-info text-center mt-4 border-0 shadow-sm">
                            <i class="bi bi-chat-square-dots fs-3 d-block mb-2 text-info"></i>
                            Aún no hay comentarios para este miembro. <br> ¡Sé el primero en dejar uno!
                        </div>`;
                    return;
                }

                // if there are comments, build the HTML to display them
                let html = '';
                data.forEach(comment => {
                    html += `
                        <div class="card mb-3 shadow-sm border-0 bg-light">
                            <div class="card-body">
                                <p class="mb-2">${comment.texto}</p>
                                <div class="d-flex justify-content-between align-items-center">
                                    <small class="text-muted"><i class="bi bi-person-fill"></i> ${comment.nombre}</small>
                                    <small class="text-muted"><i class="bi bi-clock"></i> ${comment.fecha}</small>
                                </div>
                            </div>
                        </div>
                    `;
                });
                
                // render the comments in the page
                commentsList.innerHTML = html;
            })
            .catch(error => {
                console.error('Error:', error);
                commentsList.innerHTML = `
                    <div class="alert alert-warning text-center mt-4 border-0 shadow-sm">
                        <i class="bi bi-exclamation-triangle fs-3 d-block mb-2 text-warning"></i>
                        No se pudieron cargar los comentarios en este momento.
                    </div>`;
            });
    };

    // Initial load of comments when the page is ready
    loadComments();

    const commentForm = document.getElementById('form-comment');
    commentForm.addEventListener('submit', (event) => {
        event.preventDefault();  // stop the form from submitting

        const nameInput = document.getElementById('comment-name');
        const textInput = document.getElementById('comment-text');
        const nameValue = nameInput.value.trim();
        const textValue = textInput.value.trim();
        
        const errorName = document.getElementById('error-comment-name');
        const errorText = document.getElementById('error-comment-text');
        const serverError = document.getElementById('server-error-msg');

        nameInput.classList.remove('is-invalid');
        textInput.classList.remove('is-invalid');
        errorName.style.display = 'none';
        errorText.style.display = 'none';
        serverError.classList.add('d-none');

        let isValid = true;

        // VALIDATE NAME (LENGTH 3-80)
        if (nameValue.length > 80 || nameValue.length < 3) {
            nameInput.classList.add('is-invalid');
            errorName.innerText = "El nombre debe tener entre 3 y 80 caracteres.";
            errorName.style.display = 'block';
            isValid = false;
        }

        // VALIDATE TEXT (LENGTH 5-300)
        if (textValue.length > 300 || textValue.length < 5) {
            textInput.classList.add('is-invalid');
            errorText.innerText = "El comentario debe tener entre 5 y 300 caracteres.";
            errorText.style.display = 'block';
            isValid = false;
        }

        if (!isValid) return; // if validation fails, stop here

        // If validation passes, send the comment to the server
        const btnSubmit = document.getElementById('btn-submit-comment');
        const originalBtnText = btnSubmit.innerHTML;
        btnSubmit.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Enviando...';
        btnSubmit.disabled = true;

        const payload = {
            actividad_id: actividadId,
            nombre: nameValue,
            texto: textValue
        };

        fetch('/api/comments', {   // endpoint for creating a new comment in the backend
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        })

    
        .then(response => response.json().then(data => ({ status: response.status, body: data })))
        .then(res => {
            if (res.status === 201 || res.status === 200) {
                
                commentForm.reset();
                formContainer.classList.add('d-none');
                btnToggle.classList.remove('d-none');
            
                loadComments();
                
            } else {
                // ERROR
                serverError.innerText = res.body.error || "Error al guardar el comentario en el servidor.";
                serverError.classList.remove('d-none');
            }
        })
        .catch(error => {
            console.error('Error en la petición:', error);
            serverError.innerText = "Error de conexión con el servidor.";
            serverError.classList.remove('d-none');
        })
        .finally(() => {
            btnSubmit.innerHTML = originalBtnText;
            btnSubmit.disabled = false;
        });
    });

});