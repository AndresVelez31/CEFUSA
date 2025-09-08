class LoginForm {
    // Initialize form elements and setup
    constructor() {
        this.form = document.getElementById('loginForm');
        this.usernameInput = document.getElementById('username');
        this.passwordInput = document.getElementById('password');
        this.rememberInput = document.getElementById('remember');
        this.passwordToggle = document.getElementById('passwordToggle');
        this.submitButton = this.form.querySelector('.login-btn');
        this.successMessage = document.getElementById('successMessage');
        
        this.init();
    }
    
    // Setup form functionality
    init() {
        this.bindEvents();
        this.setupPasswordToggle();
    }
    
    // Attach event listeners
    bindEvents() {
        this.form.addEventListener('submit', (e) => this.handleSubmit(e));
        this.usernameInput.addEventListener('blur', () => this.validateUsername());
        this.passwordInput.addEventListener('blur', () => this.validatePassword());
        this.usernameInput.addEventListener('input', () => this.clearError('username'));
        this.passwordInput.addEventListener('input', () => this.clearError('password'));
    }
    
    // Toggle password visibility
    setupPasswordToggle() {
        this.passwordToggle.addEventListener('click', () => {
            const isPassword = this.passwordInput.type === 'password';
            this.passwordInput.type = isPassword ? 'text' : 'password';
            this.passwordToggle.style.transform = isPassword ? 'rotate(180deg)' : 'rotate(0deg)';
        });
    }

    // Validate username field
    validateUsername() {
        const username = this.usernameInput.value.trim();
        
        if (!username) {
            this.showError('username', 'El usuario es requerido');
            return false;
        }
        
        this.clearError('username');
        return true;
    }

    // Validate password field
    validatePassword() {
        const password = this.passwordInput.value;
        
        if (!password) {
            this.showError('password', 'La contraseña es requerida');
            return false;
        }
        
        this.clearError('password');
        return true;
    }

    // Show error message for field
    showError(field, message) {
        const formGroup = document.getElementById(field).closest('.form-group');
        const errorElement = document.getElementById(`${field}Error`);
        
        formGroup.classList.add('error');
        errorElement.textContent = message;
        errorElement.classList.add('show');
    }

    // Clear error message for field
    clearError(field) {
        const formGroup = document.getElementById(field).closest('.form-group');
        const errorElement = document.getElementById(`${field}Error`);
        
        formGroup.classList.remove('error');
        errorElement.classList.remove('show');
        setTimeout(() => {
            errorElement.textContent = '';
        }, 200);
    }

    // Handle form submission
    async handleSubmit(e) {
        e.preventDefault();
        
        if (!this.isFormValid()) return;
        
        this.setLoading(true);
        
        try {
            const response = await this.submitLogin();
            await this.handleResponse(response);
        } catch (error) {
            this.showError('password', 'An error occurred. Please try again.');
        } finally {
            this.setLoading(false);
        }
    }

    // Check if form is valid
    isFormValid() {
        const isUsernameValid = this.validateUsername();
        const isPasswordValid = this.validatePassword();
        return isUsernameValid && isPasswordValid;
    }

    // Submit login request to server
    async submitLogin() {
        return await fetch('/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: JSON.stringify({
                username: this.usernameInput.value,
                password: this.passwordInput.value,
                remember: this.rememberInput.checked
            })
        });
    }

    // Handle server response
    async handleResponse(response) {
        const data = await response.json();
        
        if (response.ok && data.success) {
            this.showSuccess(data.redirect_url || '/home/');
        } else {
            this.showError('password', data.error || 'Sign in failed. Please try again.');
        }
    }

    // Set loading state
    setLoading(loading) {
        this.submitButton.classList.toggle('loading', loading);
        this.submitButton.disabled = loading;
    }

    // Show success animation and redirect
    showSuccess(redirectUrl = '/home/') {
        this.hideForm();
        this.hideOptionalElements();
        this.displaySuccessMessage();
        this.redirectAfterDelay(redirectUrl);
    }

    // Hide form with transition
    hideForm() {
        this.form.style.transform = 'scale(0.95)';
        this.form.style.opacity = '0';
        
        setTimeout(() => {
            this.form.style.display = 'none';
        }, 300);
    }

    // Hide optional login elements
    hideOptionalElements() {
        setTimeout(() => {
            const elements = [
                '.social-login',
                '.signup-link', 
                '.divider'
            ];
            
            elements.forEach(selector => {
                const element = document.querySelector(selector);
                if (element) element.style.display = 'none';
            });
        }, 300);
    }

    // Display success message
    displaySuccessMessage() {
        setTimeout(() => {
            if (this.successMessage) {
                this.successMessage.classList.add('show');
            }
        }, 300);
    }

    // Redirect to URL after delay
    redirectAfterDelay(url) {
        setTimeout(() => {
            window.location.href = url;
        }, 2500);
    }
}

// Initialize form when page loads
document.addEventListener('DOMContentLoaded', () => {
    new LoginForm();
});