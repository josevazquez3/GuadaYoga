document.addEventListener('DOMContentLoaded', function() {
    const usernameInput = document.querySelector('input[name="username"]');
    const usernameFeedback = document.getElementById('username-feedback');
    let timeoutId;

    if (usernameInput && usernameFeedback) {
        usernameInput.addEventListener('input', function() {
            clearTimeout(timeoutId);
            const username = this.value.trim();

            if (username.length > 0) {
                timeoutId = setTimeout(() => {
                    fetch('/accounts/check-username/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                        },
                        body: JSON.stringify({ username: username })
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.is_taken) {
                            usernameFeedback.textContent = 'Este nombre de usuario ya está en uso. Por favor, elige otro.';
                            usernameFeedback.classList.remove('d-none', 'alert-success');
                            usernameFeedback.classList.add('alert-warning');
                            usernameInput.classList.add('is-invalid');
                        } else {
                            usernameFeedback.textContent = 'Este nombre de usuario está disponible.';
                            usernameFeedback.classList.remove('d-none', 'alert-warning');
                            usernameFeedback.classList.add('alert-success');
                            usernameInput.classList.remove('is-invalid');
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                    });
                }, 500);
            } else {
                usernameFeedback.classList.add('d-none');
                usernameInput.classList.remove('is-invalid');
            }
        });
    }
});