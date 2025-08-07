// create appointment modal
document.addEventListener('DOMContentLoaded', function () {
    const createModal = document.getElementById('create-modal');
    const modalBody = createModal.querySelector('#create-modal-body');
    const form = createModal.querySelector('#create-form');

    createModal.addEventListener('show.bs.modal', async function (event) {
        const button = event.relatedTarget;
        const formUrl = button.getAttribute('data-form-url');
        const createUrl = button.getAttribute('data-create-url');

        modalBody.innerHTML = '<p>Carregando...</p>';

        try {
            const response = await fetch(formUrl, {
                headers: { 'X-Requested-With': 'XMLHttpRequest' }
            });
            const data = await response.json();
            modalBody.innerHTML = data.form_html;
            form.action = createUrl;
            console.log("data: ", data)
            if (window.djangoAutocompleteLight) {
                window.djangoAutocompleteLight.init();
            }
        } catch (error) {
            modalBody.innerHTML = '<p class="text-danger">Erro ao carregar o formulário.</p>';
        }
    });
});


// delete appointment modal
document.addEventListener('DOMContentLoaded', function () {
    const deleteModal = document.getElementById('delete-modal');
    const modalText = deleteModal.querySelector('#delete-modal-text');
    const form = deleteModal.querySelector('#delete-form');

    deleteModal.addEventListener('show.bs.modal', async function (event) {
        const button = event.relatedTarget;
        const pk = button.getAttribute('data-pk');
        const deleteUrl = button.getAttribute('data-delete-url');

        modalText.textContent = 'Carregando...';
        form.action = '';

        try {
            const response = await fetch(deleteUrl, {
                headers: { 'X-Requested-With': 'XMLHttpRequest' }
            });
            const data = await response.json();
            modalText.textContent = `Tem certeza que deseja excluir ${data.object_name}?`;
            form.action = data.action_url;
        } catch (error) {
            modalText.textContent = 'Erro ao carregar os dados.';
        }
    });
});


// edit appointment modal
document.addEventListener('DOMContentLoaded', function () {
    const editModal = document.getElementById('edit-modal');
    const modalBody = editModal.querySelector('#edit-modal-body');
    const form = editModal.querySelector('#update-form');

    editModal.addEventListener('show.bs.modal', async function (event) {
        const button = event.relatedTarget;
        const formUrl = button.getAttribute('data-form-url');
        const updateUrl = button.getAttribute('data-update-url');

        modalBody.innerHTML = '<p>Carregando...</p>';

        try {
            const response = await fetch(formUrl, {
                headers: { 'X-Requested-With': 'XMLHttpRequest' }
            });
            const data = await response.json();
            modalBody.innerHTML = data.form_html;
            form.action = updateUrl;
        } catch (error) {
            modalBody.innerHTML = '<p class="text-danger">Erro ao carregar o formulário.</p>';
        }
    });
});