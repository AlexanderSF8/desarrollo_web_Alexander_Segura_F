// =============================================
//  VALIDATION FUNCTIONS
// =============================================

const validateName = (name) => {
    if (!name) return false;    //requeried
    //accept letters (including accents), spaces, min 5 chars, max 50 chars
    const re = /^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]{5,50}$/; 
    return re.test(name.trim());
};

const validateEmail = (email) => {
    if (!email) return false;   // requeried
    const re = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return re.test(email.trim()) && email.length <= 60;
};

const validatePhone = (phone) => {
    if (!phone) return false;   // requiered
    // Accept(Chile format): 56912345678, +56912345678, 912345678
    const re = /^(\+?56\s?)?9\s?\d{4}\s?\d{4}$/;
    return re.test(phone.trim());
};

const validateCategory = (category) => {
    return category !== "";
};

// =============================================
// VISUAL CONTROL FUNCTIONS
// =============================================

const showError = (idInput, mensaje) => {
    const inputElement = document.getElementById(idInput);
    if (!inputElement) return;

    let errorElement = document.getElementById(`error-${idInput}`);
    if (!errorElement) {
        errorElement = document.createElement('div');
        errorElement.id = `error-${idInput}`;
        errorElement.className = 'text-danger small mt-1 error-msg'; // Bootstrap Class
        inputElement.parentNode.insertBefore(errorElement, inputElement.nextSibling);
    }

    errorElement.innerText = mensaje;
    errorElement.style.display = 'block';
    inputElement.style.border = '2px solid #dc3545';
};

const clearErrors = () => {
    const errorMessages = document.querySelectorAll('.error-msg');
    errorMessages.forEach(msg => {
        msg.style.display = 'none';
        msg.innerText = '';
    });
    const inputs = document.querySelectorAll('.form-control, .form-select');
    inputs.forEach(input => {
        input.style.border = ''; 
    });
    const errorTerminos = document.getElementById('error-terminos');
    if (errorTerminos) errorTerminos.style.display = 'none';
};

// =============================================
// VALIDATE FORM
// =============================================

document.addEventListener("DOMContentLoaded", function() {

    // catch the submit button
    const form= document.getElementById('form-register');
    
    if (form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault(); 
    
            clearErrors();

            // Get values from the form
            const name = document.getElementById('name').value;
            const email = document.getElementById('email').value;
            const phone = document.getElementById('phone').value;
            const category = document.getElementById('select-department').value;
            const terminos = document.getElementById('terminos').checked;

            let haveError = false;

            // --- VALIDATION EXECUTION ---

            if (!validateName(name)) {
                showError('name', 'Ingrese un nombre válido (solo letras, mínimo 5 caracteres).');
                haveError = true;
            }

            if (!validateEmail(email)) {
                showError('email', 'Por favor ingrese un correo electrónico válido.');
                haveError = true;
            }

            if (!validatePhone(phone)) {
                showError('phone', 'Ingrese un celular válido (Ej: 569 12345678).');
                haveError = true;
            }

            if (!validateCategory(category)) {
                showError('select-department', 'Debe seleccionar una categoría para continuar.');
                haveError = true;
            }

            if (!terminos) {
                showError('terminos', 'Debe confirmar que es parte del DCC y aceptar los términos.');
                haveError = true;
            }

            if (haveError) {
                return;
            }

            // --- EXIT: SAVE AND REDIRECT ---
            // save the category in localStorage to use it in the next page
            localStorage.setItem('selectedCategory', category);
            // Redirect to the next page 
            window.location.href = "activities.html";
        });
    }
});