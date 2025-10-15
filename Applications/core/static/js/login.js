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
    new PasswordRecovery();
});


// ==================== PASSWORD RECOVERY SYSTEM ====================

class PasswordRecovery {
    constructor() {
        // Modal elements
        this.usernameModal = document.getElementById('usernameModal');
        this.emailModal = document.getElementById('emailModal');
        this.resetPasswordModal = document.getElementById('resetPasswordModal');
        this.successResetModal = document.getElementById('successResetModal');
        
        // Forms
        this.usernameForm = document.getElementById('usernameVerificationForm');
        this.emailForm = document.getElementById('emailVerificationForm');
        this.resetPasswordForm = document.getElementById('resetPasswordForm');
        
        // Buttons
        this.forgotPasswordLink = document.getElementById('forgotPasswordLink');
        this.closeUsernameModal = document.getElementById('closeUsernameModal');
        this.closeEmailModal = document.getElementById('closeEmailModal');
        this.closeResetModal = document.getElementById('closeResetModal');
        this.backToUsernameBtn = document.getElementById('backToUsername');
        
        // Verify required elements exist
        if (!this.forgotPasswordLink || !this.usernameModal) {
            return;
        }
        
        // Inputs
        this.recoveryUsernameInput = document.getElementById('recoveryUsername');
        this.recoveryEmailInput = document.getElementById('recoveryEmail');
        this.newPassword1Input = document.getElementById('newPassword1');
        this.newPassword2Input = document.getElementById('newPassword2');
        this.maskedEmailDisplay = document.getElementById('maskedEmailDisplay');
        
        // Password toggle buttons
        this.toggleNewPassword1 = document.getElementById('toggleNewPassword1');
        this.toggleNewPassword2 = document.getElementById('toggleNewPassword2');
        
        // State
        this.maskedEmail = '';
        
        this.init();
    }
    
    init() {
        this.bindEvents();
        this.setupPasswordToggles();
        this.setupPasswordValidation();
    }
    
    bindEvents() {
        // Open password recovery flow
        this.forgotPasswordLink.addEventListener('click', (e) => {
            e.preventDefault();
            this.openUsernameModal();
        });
        
        // Close modals
        this.closeUsernameModal.addEventListener('click', () => this.closeModal(this.usernameModal));
        this.closeEmailModal.addEventListener('click', () => this.closeModal(this.emailModal));
        this.closeResetModal.addEventListener('click', () => this.closeModal(this.resetPasswordModal));
        
        // Close modals on overlay click
        [this.usernameModal, this.emailModal, this.resetPasswordModal, this.successResetModal].forEach(modal => {
            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    this.closeModal(modal);
                }
            });
        });
        
        // Back button
        this.backToUsernameBtn.addEventListener('click', () => {
            this.closeModal(this.emailModal);
            this.openUsernameModal();
        });
        
        // Form submissions
        this.usernameForm.addEventListener('submit', (e) => this.handleUsernameVerification(e));
        this.emailForm.addEventListener('submit', (e) => this.handleEmailVerification(e));
        this.resetPasswordForm.addEventListener('submit', (e) => this.handlePasswordReset(e));
        
        // Clear errors on input
        this.recoveryUsernameInput.addEventListener('input', () => this.clearError('recoveryUsername'));
        this.recoveryEmailInput.addEventListener('input', () => this.clearError('recoveryEmail'));
        this.newPassword1Input.addEventListener('input', () => this.clearError('newPassword1'));
        this.newPassword2Input.addEventListener('input', () => this.clearError('newPassword2'));
    }
    
    setupPasswordToggles() {
        [this.toggleNewPassword1, this.toggleNewPassword2].forEach((btn, index) => {
            const input = index === 0 ? this.newPassword1Input : this.newPassword2Input;
            btn.addEventListener('click', () => {
                const isPassword = input.type === 'password';
                input.type = isPassword ? 'text' : 'password';
                btn.style.transform = isPassword ? 'rotate(180deg)' : 'rotate(0deg)';
            });
        });
    }
    
    setupPasswordValidation() {
        this.newPassword1Input.addEventListener('input', () => {
            this.validatePasswordRequirements();
        });
    }
    
    validatePasswordRequirements() {
        const password = this.newPassword1Input.value;
        
        // Check each requirement
        const requirements = {
            'req-length': password.length >= 8,
            'req-uppercase': /[A-Z]/.test(password),
            'req-lowercase': /[a-z]/.test(password),
            'req-number': /\d/.test(password)
        };
        
        // Update UI for each requirement
        Object.entries(requirements).forEach(([id, isMet]) => {
            const element = document.getElementById(id);
            if (element) {
                element.classList.toggle('valid', isMet);
            }
        });
        
        return Object.values(requirements).every(val => val);
    }
    
    // Modal management
    openModal(modal) {
        modal.classList.add('show');
        document.body.style.overflow = 'hidden';
    }
    
    closeModal(modal) {
        modal.classList.remove('show');
        document.body.style.overflow = '';
        
        // Reset form in modal
        const form = modal.querySelector('form');
        if (form) {
            form.reset();
            // Clear all errors in this modal
            modal.querySelectorAll('.error-message').forEach(error => {
                error.classList.remove('show');
                error.textContent = '';
            });
            modal.querySelectorAll('.form-group').forEach(group => {
                group.classList.remove('error');
            });
        }
    }
    
    openUsernameModal() {
        this.openModal(this.usernameModal);
        this.recoveryUsernameInput.focus();
    }
    
    // Error handling
    showError(fieldId, message) {
        const input = document.getElementById(fieldId);
        const formGroup = input.closest('.form-group');
        const errorElement = document.getElementById(`${fieldId}Error`);
        
        formGroup.classList.add('error');
        errorElement.textContent = message;
        errorElement.classList.add('show');
    }
    
    clearError(fieldId) {
        const input = document.getElementById(fieldId);
        const formGroup = input.closest('.form-group');
        const errorElement = document.getElementById(`${fieldId}Error`);
        
        formGroup.classList.remove('error');
        errorElement.classList.remove('show');
        setTimeout(() => {
            errorElement.textContent = '';
        }, 200);
    }
    
    // Form submission handlers
    async handleUsernameVerification(e) {
        e.preventDefault();
        
        const username = this.recoveryUsernameInput.value.trim();
        
        if (!username) {
            this.showError('recoveryUsername', 'El nombre de usuario es requerido.');
            return;
        }
        
        const submitBtn = this.usernameForm.querySelector('.modal-btn');
        submitBtn.classList.add('loading');
        submitBtn.disabled = true;
        
        try {
            const response = await fetch('/password-recovery/verify-username/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken()
                },
                body: JSON.stringify({ username })
            });
            
            const data = await response.json();
            
            if (response.ok && data.success) {
                this.maskedEmail = data.masked_email;
                this.maskedEmailDisplay.textContent = data.masked_email;
                
                // Move to next step
                this.closeModal(this.usernameModal);
                this.openModal(this.emailModal);
                this.recoveryEmailInput.focus();
            } else {
                this.showError('recoveryUsername', data.error || 'Error al verificar el usuario.');
            }
        } catch (error) {
            this.showError('recoveryUsername', 'Error de conexión. Intente nuevamente.');
        } finally {
            submitBtn.classList.remove('loading');
            submitBtn.disabled = false;
        }
    }
    
    async handleEmailVerification(e) {
        e.preventDefault();
        
        const email = this.recoveryEmailInput.value.trim().toLowerCase();
        
        if (!email) {
            this.showError('recoveryEmail', 'El correo electrónico es requerido.');
            return;
        }
        
        if (!this.isValidEmail(email)) {
            this.showError('recoveryEmail', 'Ingrese un correo electrónico válido.');
            return;
        }
        
        const submitBtn = this.emailForm.querySelector('.modal-btn');
        submitBtn.classList.add('loading');
        submitBtn.disabled = true;
        
        try {
            const response = await fetch('/password-recovery/verify-email/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken()
                },
                body: JSON.stringify({ email })
            });
            
            const data = await response.json();
            
            if (response.ok && data.success) {
                // Move to password reset step
                this.closeModal(this.emailModal);
                this.openModal(this.resetPasswordModal);
                this.newPassword1Input.focus();
            } else {
                this.showError('recoveryEmail', data.error || 'El correo no coincide.');
            }
        } catch (error) {
            this.showError('recoveryEmail', 'Error de conexión. Intente nuevamente.');
        } finally {
            submitBtn.classList.remove('loading');
            submitBtn.disabled = false;
        }
    }
    
    async handlePasswordReset(e) {
        e.preventDefault();
        
        const password1 = this.newPassword1Input.value;
        const password2 = this.newPassword2Input.value;
        
        // Validate passwords
        if (!password1 || !password2) {
            if (!password1) this.showError('newPassword1', 'La contraseña es requerida.');
            if (!password2) this.showError('newPassword2', 'Confirme la contraseña.');
            return;
        }
        
        if (password1 !== password2) {
            this.showError('newPassword2', 'Las contraseñas no coinciden.');
            return;
        }
        
        if (!this.validatePasswordRequirements()) {
            this.showError('newPassword1', 'La contraseña no cumple con los requisitos.');
            return;
        }
        
        const submitBtn = this.resetPasswordForm.querySelector('.modal-btn');
        submitBtn.classList.add('loading');
        submitBtn.disabled = true;
        
        try {
            const response = await fetch('/password-recovery/reset-password/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken()
                },
                body: JSON.stringify({ 
                    password1, 
                    password2 
                })
            });
            
            const data = await response.json();
            
            if (response.ok && data.success) {
                // Show success modal
                this.closeModal(this.resetPasswordModal);
                this.openModal(this.successResetModal);
                
                // Redirect to login after delay
                setTimeout(() => {
                    this.closeModal(this.successResetModal);
                    window.location.reload();
                }, 3000);
            } else {
                this.showError('newPassword1', data.error || 'Error al actualizar la contraseña.');
            }
        } catch (error) {
            this.showError('newPassword1', 'Error de conexión. Intente nuevamente.');
        } finally {
            submitBtn.classList.remove('loading');
            submitBtn.disabled = false;
        }
    }
    
    // Utility functions
    getCSRFToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    }
    
    isValidEmail(email) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }
}