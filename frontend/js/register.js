document.getElementById('registerForm')?.addEventListener('submit', async (event) => {
    event.preventDefault();
    const message = document.getElementById('registerMessage');
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    message.className = 'alert d-none';

    if (password !== confirmPassword) {
        message.textContent = 'Passwords do not match.';
        message.className = 'alert alert-danger';
        return;
    }

    try {
        const apiBaseUrl = '/api';
        const response = await fetch(`${apiBaseUrl}/users/register/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                username: document.getElementById('username').value,
                email: document.getElementById('email').value,
                first_name: document.getElementById('firstName').value,
                last_name: document.getElementById('lastName').value,
                phone: document.getElementById('phone').value,
                password,
                role: 'customer'
            })
        });
        const data = await response.json();
        if (!response.ok) {
            const firstError = Object.values(data)[0];
            throw new Error(Array.isArray(firstError) ? firstError[0] : 'Registration failed.');
        }
        message.textContent = data.message;
        message.className = 'alert alert-success';
        event.target.reset();
        setTimeout(() => { window.location.href = 'login.html'; }, 1200);
    } catch (error) {
        message.textContent = error.message;
        message.className = 'alert alert-danger';
    }
});