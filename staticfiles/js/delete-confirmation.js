document.addEventListener('DOMContentLoaded', function () {
    const deleteButton = document.querySelector('.btn-danger');
    if (deleteButton) {
        deleteButton.addEventListener('click', function (event) {
            const confirmation = confirm("Are you sure you want to delete your profile? This action cannot be undone.");
            if (!confirmation) {
                event.preventDefault();
            }
        });
    }
});