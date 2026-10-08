/**
 * API Client - Handles all HTTP requests to the backend
 */

const API_BASE_URL = '/api';

class APIClient {
    constructor() {
        this.token = localStorage.getItem('access_token');
    }

    async patch(endpoint, data = {}) {
        try {
            const response = await fetch(`${API_BASE_URL}${endpoint}`, {
                method: 'PATCH',
                headers: this.getHeaders(),
                body: JSON.stringify(data),
            });

            return this.handleResponse(response);
        } catch (error) {
            console.error('PATCH request failed:', error);
            throw error;
        }
    }

    /**
     * Set authentication token
     */
    setToken(token) {
        this.token = token;
        localStorage.setItem('access_token', token);
    }

    /**
     * Get default headers
     */
    getHeaders() {
        const headers = {
            'Content-Type': 'application/json',
        };
        if (this.token) {
            headers['Authorization'] = `Bearer ${this.token}`;
        }
        return headers;
    }

    /**
     * Generic GET request
     */
    async get(endpoint, params = {}) {
        try {
            const url = new URL(`${API_BASE_URL}${endpoint}`, window.location.origin);
            Object.keys(params).forEach(key => url.searchParams.append(key, params[key]));
            
            const response = await fetch(url, {
                method: 'GET',
                headers: this.getHeaders(),
            });
            
            return this.handleResponse(response);
        } catch (error) {
            console.error('GET request failed:', error);
            throw error;
        }
    }

    /**
     * Generic POST request
     */
    async post(endpoint, data = {}) {
        try {
            const response = await fetch(`${API_BASE_URL}${endpoint}`, {
                method: 'POST',
                headers: this.getHeaders(),
                body: JSON.stringify(data),
            });
            
            return this.handleResponse(response);
        } catch (error) {
            console.error('POST request failed:', error);
            throw error;
        }
    }

    /**
     * Generic PUT request
     */
    async put(endpoint, data = {}) {
        try {
            const response = await fetch(`${API_BASE_URL}${endpoint}`, {
                method: 'PUT',
                headers: this.getHeaders(),
                body: JSON.stringify(data),
            });
            
            return this.handleResponse(response);
        } catch (error) {
            console.error('PUT request failed:', error);
            throw error;
        }
    }

    /**
     * Generic DELETE request
     */
    async delete(endpoint) {
        try {
            const response = await fetch(`${API_BASE_URL}${endpoint}`, {
                method: 'DELETE',
                headers: this.getHeaders(),
            });
            
            if (response.status === 204) {
                return { success: true };
            }
            
            return this.handleResponse(response);
        } catch (error) {
            console.error('DELETE request failed:', error);
            throw error;
        }
    }

    /**
     * Handle API response
     */
    async handleResponse(response) {
        if (response.status === 401) {
            // Unauthorized - clear token and redirect to login
            localStorage.removeItem('access_token');
            window.location.href = '/pages/login.html';
            return;
        }

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'API request failed');
        }

        if (response.status === 204) {
            return { success: true };
        }

        return await response.json();
    }

    // Authentication Endpoints
    login(username, password) {
        return this.post('/token/', { username, password });
    }

    getCurrentUser() {
        return this.get('/users/me/');
    }

    logout() {
        localStorage.removeItem('access_token');
    }

    // Vehicle Endpoints
    getVehicles(params = {}) {
        return this.get('/vehicles/', params);
    }

    getVehicle(id) {
        return this.get(`/vehicles/${id}/`);
    }

    createVehicle(data) {
        return this.post('/vehicles/', data);
    }

    updateVehicle(id, data) {
        return this.put(`/vehicles/${id}/`, data);
    }

    deleteVehicle(id) {
        return this.delete(`/vehicles/${id}/`);
    }

    // Driver Endpoints
    getDrivers(params = {}) {
        return this.get('/drivers/', params);
    }

    getDriver(id) {
        return this.get(`/drivers/${id}/`);
    }

    createDriver(data) {
        return this.post('/drivers/', data);
    }

    updateDriver(id, data) {
        return this.put(`/drivers/${id}/`, data);
    }

    // Trip Endpoints
    getTrips(params = {}) {
        return this.get('/trips/', params);
    }

    getTrip(id) {
        return this.get(`/trips/${id}/`);
    }

    createTrip(data) {
        return this.post('/trips/', data);
    }

    updateTrip(id, data) {
        return this.put(`/trips/${id}/`, data);
    }

    // Fuel Endpoints
    getFuelEntries(params = {}) {
        return this.get('/fuel/entries/', params);
    }

    createFuelEntry(data) {
        return this.post('/fuel/entries/', data);
    }

    // Maintenance Endpoints
    getMaintenanceRecords(params = {}) {
        return this.get('/maintenance/records/', params);
    }

    createMaintenanceRecord(data) {
        return this.post('/maintenance/records/', data);
    }

    // Dashboard Endpoints
    getDashboardStats() {
        return this.get('/dashboard/');
    }

    // Reports Endpoints
    getReports(params = {}) {
        return this.get('/reports/', params);
    }

    generateReport(data) {
        return this.post('/reports/', data);
    }
}

// Create global instance
const apiClient = new APIClient();
