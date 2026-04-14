document.addEventListener("DOMContentLoaded", function() {
    
    // Catching elements from the DOM
    const searchInput = document.getElementById('search-input');
    const filterType = document.getElementById('filter-type');
    const sortOrder = document.getElementById('sort-order');
    const paginationControls = document.getElementById('pagination-controls');
    
    // Get all member cards as an array for easier manipulation
    const allCards = Array.from(document.querySelectorAll('.member-card'));
    
    // PAGINATION VARIABLES
    let currentPage = 1;
    const cardsPerPage = 2; // Show 2 card for page

    // ==========================================
    // PRINCIPAL LOGIC FUNCTIONS
    // ==========================================
    const updateView = () => {
        const searchTerm = searchInput.value.toLowerCase();
        const selectedType = filterType.value;
        const selectedSort = sortOrder.value;

        let visibleCards = allCards.filter(card => {
            // search and filter logic
            const cardText = card.innerText.toLowerCase();
            const cardType = card.getAttribute('data-type'); // 'estudiante', 'docente', etc.

            const matchesSearch = cardText.includes(searchTerm);
            const matchesType = (selectedType === 'todos') || (cardType === selectedType);

            return matchesSearch && matchesType;
        });

        visibleCards.sort((a, b) => {
            const nameA = a.getAttribute('data-name').toLowerCase();
            const nameB = b.getAttribute('data-name').toLowerCase();
            
            if (selectedSort === 'az') return nameA.localeCompare(nameB);
            if (selectedSort === 'za') return nameB.localeCompare(nameA);
            return 0;
        });

        // Pageination logic
        const totalPages = Math.ceil(visibleCards.length / cardsPerPage);
        if (currentPage > totalPages) currentPage = totalPages || 1; 

        const startIndex = (currentPage - 1) * cardsPerPage;
        const endIndex = startIndex + cardsPerPage;

        // Rendering cards logic 
        allCards.forEach(card => card.classList.add('d-none'));
        // Show only the cards that correspond to the current page
        const cardsToShow = visibleCards.slice(startIndex, endIndex);
        cardsToShow.forEach(card => card.classList.remove('d-none'));

        // Update pagination buttons
        renderPagination(totalPages);
    };

    // ==========================================
    // DRAW PAGINATION
    // ==========================================
    const renderPagination = (totalPages) => {
        // clear previous buttons
        paginationControls.innerHTML = '';

        if (totalPages <= 1) return; // if there's only 1 page, no need to show pagination

        // Previous button
        const prevDisabled = currentPage === 1 ? 'disabled' : '';
        paginationControls.innerHTML += `
            <li class="page-item ${prevDisabled}">
                <a class="page-link" role="button" data-page="${currentPage - 1}">Anterior</a>
            </li>
        `;

        for (let i = 1; i <= totalPages; i++) {
            const activeClass = currentPage === i ? 'active' : '';
            paginationControls.innerHTML += `
                <li class="page-item ${activeClass}">
                    <a class="page-link" role="button" data-page="${i}">${i}</a>
                </li>
            `;
        }

        // Next button
        const nextDisabled = currentPage === totalPages ? 'disabled' : '';
        paginationControls.innerHTML += `
            <li class="page-item ${nextDisabled}">
                <a class="page-link" role="button" data-page="${currentPage + 1}">Siguiente</a>
            </li>
        `;

        // get logic for pagination buttons
        const pageLinks = paginationControls.querySelectorAll('.page-link');
        pageLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault(); // prevent default anchor behavior
                const parentLi = e.target.parentElement;
                
                if (!parentLi.classList.contains('disabled') && !parentLi.classList.contains('active')) {
                    currentPage = parseInt(e.target.getAttribute('data-page'));
                    updateView(); // update the view with the new page
                }
            });
        });
    };

    // ==========================================
    // EVENT LISTENERS
    // ==========================================
    
    // if the user types in the search input, we update the view
    searchInput.addEventListener('input', () => {
        currentPage = 1;
        updateView();
    });

    // if the filter changes, we go back to page 1 and update the view
    filterType.addEventListener('change', () => {
        currentPage = 1;
        updateView();
    });

    // if the sort order changes, we update the view
    sortOrder.addEventListener('change', () => {
        updateView();
    });

    // Every time the page loads, we want to show the first page with the default filters
    updateView();
});