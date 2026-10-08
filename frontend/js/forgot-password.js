const requestResetForm = document.getElementById('requestResetForm');
const resetPasswordForm = document.getElementById('resetPasswordForm');
const resetMessage = document.getElementById('resetMessage');
const apiBaseUrl = '/api';
const resetParams = new URLSearchParams(window.location.search);
const resetCredentials = {
    uid: resetParams.get('uid'),
    token: resetParams.get('token'),
};

if (resetCredentials.uid && resetCredentials.token) {
    requestResetForm.hidden = true;
    resetPasswordForm.hidden = false;
    document.getElementById('resetInstructions').textContent = 'Choose a new password for your account.';
}

requestResetForm?.addEventListener('submit', async (event) => {
    event.preventDefault();
    const button = event.target.querySelector('button[type="submit"]');

    resetMessage.className = 'alert d-none';
    button.disabled = true;
    button.textContent = 'Sending...';

    try {
        const requestResponse = await fetch(`${apiBaseUrl}/users/password-reset/request/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ identifier: document.getElementById('identifier').value })
        });
        const responseData = await requestResponse.json();
        if (!requestResponse.ok) {
            throw new Error(responseData.detail || 'Unable to process the request.');
        }

        resetMessage.textContent = responseData.message;
        resetMessage.className = 'alert alert-success';
    } catch (error) {
        resetMessage.textContent = error.message;
        resetMessage.className = 'alert alert-danger';
    } finally {
        button.disabled = false;
        button.textContent = 'Send reset link';
    }
});

resetPasswordForm?.addEventListener('submit', async (event) => {
    event.preventDefault();
    const button = event.target.querySelector('button[type="submit"]');
    const newPassword = document.getElementById('newPassword').value;
    const confirmPassword = document.getElementById('confirmPassword').value;

    resetMessage.className = 'alert d-none';
    if (newPassword !== confirmPassword) {
        resetMessage.textContent = 'Passwords do not match.';
        resetMessage.className = 'alert alert-danger';
        return;
    }

    button.disabled = true;
    button.textContent = 'Resetting...';

    try {
        const response = await fetch(`${apiBaseUrl}/users/password-reset/confirm/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ ...resetCredentials, new_password: newPassword })
        });
        const responseData = await response.json();
        if (!response.ok) {
            throw new Error(responseData.detail || 'Password reset failed.');
        }

        resetMessage.textContent = responseData.message;
        resetMessage.className = 'alert alert-success';
        event.target.reset();
        setTimeout(() => { window.location.href = 'login.html'; }, 1200);
    } catch (error) {
        resetMessage.textContent = error.message;
        resetMessage.className = 'alert alert-danger';
        button.disabled = false;
        button.textContent = 'Reset password';
    }
});
