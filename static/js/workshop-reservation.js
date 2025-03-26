document.addEventListener('DOMContentLoaded', function() {
    const reservationForms = document.querySelectorAll('.workshop-reservation-form');

    reservationForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(form);
            const submitButton = form.querySelector('button[type="submit"]');
            const successAlert = form.querySelector('.alert-success');
            const errorAlert = form.querySelector('.alert-danger');
            const modal = form.closest('.modal');

            // Disable submit button and show loading state
            submitButton.disabled = true;
            submitButton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Enviando...';

            // Reset alerts
            successAlert.classList.add('d-none');
            errorAlert.classList.add('d-none');

            fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Show success message
                    successAlert.textContent = 'Reserva enviada exitosamente';
                    successAlert.classList.remove('d-none');
                    
                    // Reset form
                    form.reset();
                    
                    // Close modal and redirect to home page after 2 seconds
                    setTimeout(() => {
                        const modalInstance = bootstrap.Modal.getInstance(modal);
                        modalInstance.hide();
                        // Reset button state
                        submitButton.disabled = false;
                        submitButton.innerHTML = 'Enviar Reserva';
                        // Redirect to home page
                        window.location.href = '/';                        
                    }, 2000);
                } else {
                    throw new Error(data.message || 'Error al enviar la reserva');
                }
            })
            .catch(error => {
                // Show error message
                errorAlert.textContent = error.message;
                errorAlert.classList.remove('d-none');
                
                // Reset button state
                submitButton.disabled = false;
                submitButton.innerHTML = 'Enviar Reserva';
            });
        });
    });
});