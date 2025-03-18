document.addEventListener('DOMContentLoaded', function() {
    // Handle Create Video Modal
    const createButton = document.querySelector('[data-bs-target="#createVideoModal"]');
    if (createButton) {
        createButton.addEventListener('click', function() {
            const form = document.querySelector('#createVideoModal form');
            form.reset(); // Reset form when opening modal
        });
    }

    // Handle Edit Video Modal
    const editButtons = document.querySelectorAll('[data-bs-target^="#editVideoModal"]');
    editButtons.forEach(button => {
        button.addEventListener('click', function() {
            const videoId = this.getAttribute('data-bs-target').replace('#editVideoModal', '');
            const form = document.querySelector(`#editVideoModal${videoId} form`);
            form.action = `/videos/${videoId}/edit/`;

            // Pre-fill the form with current video data
            const card = this.closest('.card');
            const title = card.querySelector('.card-title').textContent;
            const summary = card.querySelector('.card-text').textContent;
            const videoContainer = card.querySelector('.embed-responsive iframe');
            const videoUrl = videoContainer ? videoContainer.src : '';

            form.querySelector('#edit_title').value = title;
            form.querySelector('#edit_summary').value = summary;
            form.querySelector('#edit_url').value = videoUrl;
        });
    });

    // Handle Delete Video Modal
    const deleteButtons = document.querySelectorAll('[data-bs-target^="#deleteVideoModal"]');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function() {
            const videoId = this.getAttribute('data-bs-target').replace('#deleteVideoModal', '');
            const form = document.querySelector(`#deleteVideoModal${videoId} form`);
            form.action = `/videos/${videoId}/delete/`;
        });
    });
});