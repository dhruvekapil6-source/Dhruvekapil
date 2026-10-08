/**
 * Authentication JavaScript
 */

document.getElementById('loginForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const button = e.target.querySelector('button[type="submit"]');
    const message = document.getElementById('loginMessage');

    message.className = 'alert d-none';
    button.disabled = true;
    button.textContent = 'Signing in...';

    try {
        const apiBaseUrl = '/api';
        const response = await fetch(`${apiBaseUrl}/token/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password }),
        });

        if (!response.ok) {
            throw new Error('Login failed');
        }

        const data = await response.json();
        
        // Store tokens
        localStorage.setItem('access_token', data.access);
        if (data.refresh) {
            localStorage.setItem('refresh_token', data.refresh);
        }

        // Redirect to dashboard
        window.location.href = 'dashboard.html';
    } catch (error) {
        console.error('Login error:', error);
        message.textContent = 'The username or password is incorrect.';
        message.className = 'alert alert-danger';
        button.disabled = false;
        button.textContent = 'Login';
    }
});
