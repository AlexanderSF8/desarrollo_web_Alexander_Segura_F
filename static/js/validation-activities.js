// =============================================
// VALIDATION FUNCTIONS
// =============================================

const validateText = (text, minLength) => {
    if (!text) return false;    //required
    return text.trim().length >= minLength;
};

const validateNumber = (num, min, max) => {
    if (!num || isNaN(num)) return false; // required 
    const value = Number(num);
    return value >= min && value <= max;
};

const validateTelegram = (telegram) => {
    if (!telegram) return true;    // optional
    const re = /^@[a-zA-Z0-9_]{4,32}$/;
    return re.test(telegram.trim());
};

const validateURL = (url) => {
    if (!url) return true; // optional 
    const re = /^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$/;
    return re.test(url.trim());
};

const validateCheckboxes = (name) => {
    const checkboxes = document.querySelectorAll(`input[name="${name}"]:checked`);
    return checkboxes.length > 0;
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
        // w-100 obliga al texto a usar una línea nueva para no chocar con nada
        errorElement.className = 'text-danger small mt-1 error-msg w-100'; 
        
        // --- MAGIA PARA NO ROMPER BOOTSTRAP ---
        if (inputElement.closest('.input-group')) {
            // Si está en un input-group (ej: días/horas), lo ponemos debajo del grupo entero
            const inputGroup = inputElement.closest('.input-group');
            inputGroup.parentNode.insertBefore(errorElement, inputGroup.nextSibling);
        } else if (inputElement.closest('.form-check')) {
            // Si es un radio o checkbox, lo ponemos debajo de su fila
            const formCheck = inputElement.closest('.form-check');
            formCheck.parentNode.insertBefore(errorElement, formCheck.nextSibling);
        } else {
            // Comportamiento normal para inputs de texto normales
            inputElement.parentNode.insertBefore(errorElement, inputElement.nextSibling);
        }
    }

    errorElement.innerText = mensaje;
    errorElement.style.display = 'block';
    
    // Efecto visual de error (los checkboxes se ven raros con "border", mejor usar "outline")
    if (inputElement.type === 'radio' || inputElement.type === 'checkbox') {
        inputElement.style.outline = '2px solid #dc3545';
        inputElement.style.outlineOffset = '2px';
    } else {
        inputElement.style.border = '2px solid #dc3545'; 
    }
};

const clearErrors = () => {
    const errorMessages = document.querySelectorAll('.error-msg');
    errorMessages.forEach(msg => {
        msg.style.display = 'none';
        msg.innerText = '';
    });
    const inputs = document.querySelectorAll('.form-control, .form-check-input');
    inputs.forEach(input => {
        input.style.border = ''; 
    });
};

// =============================================
// VALIDATE FORM
// =============================================

document.addEventListener("DOMContentLoaded", function() {
    
    // --- Show/Hide Blocks Logic ---
    const studentBlock = document.getElementById('student-activities');
    const staffBlock = document.getElementById('staff-activities');
    const teachingBlock = document.getElementById('teaching-activities');
    
    studentBlock.classList.add('d-none');
    staffBlock.classList.add('d-none');
    teachingBlock.classList.add('d-none');

    // Get the category from localStorage (set in the previous page)
    const categoryUser = document.getElementById('user-category').value;

    // Show the corresponding block based on the category
    if (categoryUser === 'estudiante') studentBlock.classList.remove('d-none');
    if (categoryUser === 'funcionario') staffBlock.classList.remove('d-none');
    if (categoryUser === 'academico') teachingBlock.classList.remove('d-none');

    const selectedCategory = categoryUser; // Ahora usa la variable inyectada

    // --- VALIDATION LOGIC ---
    const form = document.querySelector('#form-activities');
    
    if (form) {
        form.addEventListener("submit", function(event) {
            clearErrors();

            let haveError = false;

            // Specific validations based on category
            if (selectedCategory === 'estudiante') {
                if (!validateCheckboxes('nivel_academico')) {
                    showError('postgrado', 'Seleccione su nivel académico.');
                    haveError = true;
                }
                const año = document.getElementById('año_ingreso').value;
                if (!validateNumber(año, 2000, 2026)) {
                    showError('año_ingreso', 'Ingrese un año válido (ej: 2023).');
                    haveError = true;
                }
                const telegram = document.getElementById('telegram').value;
                if (!validateTelegram(telegram)) {
                    showError('telegram', 'El usuario debe empezar con @ y tener al menos 4 caracteres.');
                    haveError = true;
                }
            }

            if (selectedCategory === 'funcionario') {
                if (!validateText(document.getElementById('cargo').value, 3)) {
                    showError('cargo', 'Ingrese un cargo válido.');
                    haveError = true;
                }
                if (!validateText(document.getElementById('area').value, 3)) {
                    showError('area', 'Ingrese un área de trabajo válida.');
                    haveError = true;
                }
            }

            if (selectedCategory === 'academico') {
                if (!validateText(document.getElementById('ramos').value, 3)) {
                    showError('ramos', 'Debe ingresar al menos un ramo.');
                    haveError = true;
                }
                if (!validateText(document.getElementById('investigacion').value, 3)) {
                    showError('investigacion', 'Ingrese su área de investigación.');
                    haveError = true;
                }
            }

            //  Validations common for all categories
            if (!validateCheckboxes('actividades')) {
                showError('act_recreativa', 'Debe seleccionar al menos una actividad.');
                haveError = true;
            }

            if (!validateText(document.getElementById('activity').value, 10)) {
                showError('activity', 'La descripción debe tener al menos 10 caracteres.');
                haveError = true;
            }

            const dias = document.getElementById('dias_semana').value;
            if (!validateNumber(dias, 1, 7)) {
                showError('dias_semana', 'Debe ser entre 1 y 7 días.');
                haveError = true;
            }

            const horas = document.getElementById('horas_dia').value;
            if (!validateNumber(horas, 0.5, 24)) {
                showError('horas_dia', 'Debe ser entre 0.5 y 24 horas.');
                haveError = true;
            }

            const archivos = document.getElementById('archivos').files;
            if (archivos.length === 0) {
                showError('archivos', 'Debe subir al menos un archivo (foto/video).');
                haveError = true;
            }
            
            const enlace = document.getElementById('enlace').value;
            if (enlace && !validateURL(enlace)) {
                showError('enlace', 'Si incluye un enlace, debe ser una URL válida (ej: https://...).');
                haveError = true;
            }

            if (haveError) {
                event.preventDefault(); // prevent form submission if there are errors
                window.scrollTo({ top: 0, behavior: 'smooth' });
                return;
            }

            const activityType = Array.from(document.querySelectorAll('input[name=actividades]:checked')).map(el => el.value);
            localStorage.setItem('selectedActivities', JSON.stringify(activityType));
            
        });
    }
});