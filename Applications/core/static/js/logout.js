class LogoutHandler {
    // Initialize logout functionality
    constructor() {
        this.modal = null;
        this.init();
    }

    // Setup modal instance
    init() {
        const modalElement = document.getElementById('logoutModal');
        if (modalElement) {
            this.modal = new bootstrap.Modal(modalElement);
        }
    }

    // Show logout confirmation modal
    confirmLogout() {
        if (this.modal) {
            this.modal.show();
        }
    }

    // Execute logout request
    async performLogout() {
        try {
            const response = await this.sendLogoutRequest();
            this.handleLogoutResponse(response);
        } catch (error) {
            console.error('Logout error:', error);
            this.redirectToLogin();
        }
    }

    // Send logout request to server
    async sendLogoutRequest() {
        return await fetch('/logout/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.getCSRFToken()
            }
        });
    }

    // Handle logout response
    handleLogoutResponse(response) {
        if (response.ok || response.redirected) {
            this.redirectToLogin();
        } else {
            console.error('Logout failed');
            this.redirectToLogin();
        }
    }

    // Get CSRF token from DOM or cookies
    getCSRFToken() {
        const tokenInput = document.querySelector('[name=csrfmiddlewaretoken]');
        return tokenInput?.value || this.getCookie('csrftoken');
    }

    // Extract cookie value by name
    getCookie(name) {
        if (!document.cookie) return null;
        
        const cookies = document.cookie.split(';');
        for (const cookie of cookies) {
            const [cookieName, cookieValue] = cookie.trim().split('=');
            if (cookieName === name) {
                return decodeURIComponent(cookieValue);
            }
        }
        return null;
    }

    // Redirect to login page
    redirectToLogin() {
        window.location.href = '/login/';
    }
}

// Initialize logout handler
const logoutHandler = new LogoutHandler();

// Global functions for template compatibility
function confirmLogout() {
    logoutHandler.confirmLogout();
}

function performLogout() {
    logoutHandler.performLogout();
}
