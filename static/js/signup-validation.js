document.addEventListener('DOMContentLoaded', function() {
    const signupForm = document.getElementById('signupForm');
    const usernameInput = document.querySelector('input[name="username"]');
    const usernameFeedback = document.getElementById('username-feedback');
    let usernameTimeout;

    if (usernameInput && usernameFeedback) {
        usernameInput.addEventListener('input', function() {
            clearTimeout(usernameTimeout);
            const username = this.value.trim();

            if (username.length > 0) {
                usernameTimeout = setTimeout(() => {
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
                        if (data.exists) {
                            usernameFeedback.classList.remove('d-none');
                            usernameInput.classList.add('is-invalid');
                            signupForm.querySelector('button[type="submit"]').disabled = true;
                        } else {
                            usernameFeedback.classList.add('d-none');
                            usernameInput.classList.remove('is-invalid');
                            signupForm.querySelector('button[type="submit"]').disabled = false;
                        }
                    })
                    .catch(error => console.error('Error:', error));
                }, 500);
            } else {
                usernameFeedback.classList.add('d-none');
                usernameInput.classList.remove('is-invalid');
                signupForm.querySelector('button[type="submit"]').disabled = false;
            }
        });
    }
});