/**
 * Dashboard JavaScript
 */

document.addEventListener('DOMContentLoaded', async () => {
    // Check authentication
    if (!localStorage.getItem('access_token')) {
        window.location.href = '/pages/login.html';
        return;
    }

    initFleetMap();
    document.getElementById('toggle-sidebar')?.addEventListener('click', () => document.querySelector('.sidebar').classList.toggle('active'));
    document.getElementById('map-status-filter')?.addEventListener('change', renderVehicleMap);
    document.getElementById('refresh-map')?.addEventListener('click', loadVehicleMap);

    // Load dashboard data
    await loadDashboardStats();
    loadRecentTrips();
    loadVehicleMap();
    loadCurrentUser();
});

let fleetMap;
let vehicleMarkers = [];
let mappedVehicles = [];

async function loadCurrentUser() {
    try {
        const profile = await apiClient.getCurrentUser();
        const name = profile.user?.first_name || profile.user?.username;
        if (name) document.getElementById('dashboard-user-name').textContent = name;
        if (profile.user?.username) document.getElementById('user-name').textContent = profile.user.username;
    } catch (error) {
        console.error('Failed to load current user:', error);
    }
}

function initFleetMap() {
    fleetMap = L.map('fleet-map', { zoomControl: false }).setView([20, 0], 2);
    L.control.zoom({ position: 'bottomright' }).addTo(fleetMap);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors',
        maxZoom: 19
    }).addTo(fleetMap);
}

async function loadVehicleMap() {
    const list = document.getElementById('vehicle-location-list');
    try {
        const response = await apiClient.getVehicles({ limit: 100 });
        mappedVehicles = (response.results || response).filter(vehicle => {
            const latitude = Number(vehicle.latitude);
            const longitude = Number(vehicle.longitude);
            return vehicle.latitude !== null && vehicle.latitude !== ''
                && vehicle.longitude !== null && vehicle.longitude !== ''
                && Number.isFinite(latitude) && Number.isFinite(longitude)
                && latitude >= -90 && latitude <= 90 && longitude >= -180 && longitude <= 180;
        });
        renderVehicleMap();
    } catch (error) {
        console.error('Failed to load vehicle locations:', error);
        list.innerHTML = '<p class="empty-state">Vehicle locations are unavailable right now.</p>';
    }
}

function renderVehicleMap() {
    if (!fleetMap) return;
    const filter = document.getElementById('map-status-filter').value;
    const vehicles = mappedVehicles.filter(vehicle => filter === 'all' || vehicle.status === filter);
    vehicleMarkers.forEach(marker => marker.remove());
    vehicleMarkers = vehicles.map(vehicle => {
        const marker = L.marker([vehicle.latitude, vehicle.longitude]).addTo(fleetMap);
        marker.bindPopup(`<strong>${escapeHtml(vehicle.vehicle_number)}</strong><br>${escapeHtml(vehicle.current_location || 'Location available')}<br><span class="map-popup-status">${escapeHtml(vehicle.status)}</span>`);
        return marker;
    });

    document.getElementById('mapped-vehicle-count').textContent = vehicles.length;
    document.getElementById('vehicle-location-list').innerHTML = vehicles.length
        ? vehicles.map(vehicle => `<button class="vehicle-location-item" type="button" data-lat="${vehicle.latitude}" data-lng="${vehicle.longitude}"><span class="status-dot status-${vehicle.status}"></span><span><strong>${escapeHtml(vehicle.vehicle_number)}</strong><small>${escapeHtml(vehicle.current_location || 'Coordinates available')}</small></span><i class="fas fa-chevron-right"></i></button>`).join('')
        : '<p class="empty-state">No vehicles with coordinates match this filter.</p>';

    document.querySelectorAll('.vehicle-location-item').forEach(item => item.addEventListener('click', () => {
        fleetMap.setView([item.dataset.lat, item.dataset.lng], 13);
    }));
    if (vehicles.length > 1) {
        fleetMap.fitBounds(L.latLngBounds(vehicles.map(vehicle => [vehicle.latitude, vehicle.longitude])), { padding: [30, 30], maxZoom: 12 });
    } else if (vehicles.length === 1) {
        fleetMap.setView([vehicles[0].latitude, vehicles[0].longitude], 13);
    }
}

function escapeHtml(value) {
    return String(value).replace(/[&<>'"]/g, character => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' }[character]));
}

/**
 * Load dashboard statistics
 */
async function loadDashboardStats() {
    try {
        const stats = await apiClient.getDashboardStats();
        
        // Update vehicle stats
        document.getElementById('total-vehicles').textContent = stats.vehicles.total;
        document.getElementById('active-vehicles').textContent = `${stats.vehicles.active} Active`;
        
        // Update trip stats
        document.getElementById('active-trips').textContent = stats.trips.active;
        document.getElementById('total-trips').textContent = `${stats.trips.total} Total`;
        
        // Update fuel cost
        document.getElementById('fuel-cost').textContent = `$${stats.fuel.total_cost.toFixed(2)}`;
        
        // Update maintenance cost
        document.getElementById('maintenance-cost').textContent = `$${stats.maintenance.total_cost.toFixed(2)}`;
        
        // Initialize charts
        initCharts(stats);
    } catch (error) {
        console.error('Failed to load dashboard stats:', error);
        alert('Failed to load dashboard data');
    }
}

/**
 * Load recent trips
 */
async function loadRecentTrips() {
    try {
        const trips = await apiClient.getTrips({ limit: 5 });
        const tbody = document.getElementById('recent-trips-table');
        
        if (trips.results && trips.results.length > 0) {
            tbody.innerHTML = trips.results.map(trip => `
                <tr>
                    <td>${escapeHtml(trip.trip_id)}</td>
                    <td>${escapeHtml(trip.driver)}</td>
                    <td>${escapeHtml(trip.vehicle)}</td>
                    <td><span class="badge badge-${getStatusBadgeClass(trip.status)}">${escapeHtml(trip.status)}</span></td>
                    <td>${trip.actual_distance || trip.distance} km</td>
                    <td>
                        <button class="btn btn-sm btn-primary" onclick="viewTrip(${trip.id})">View</button>
                    </td>
                </tr>
            `).join('');
        } else {
            tbody.innerHTML = '<tr><td colspan="6" class="text-center">No trips found</td></tr>';
        }
    } catch (error) {
        console.error('Failed to load recent trips:', error);
    }
}

/**
 * Get status badge class
 */
function getStatusBadgeClass(status) {
    const statusMap = {
        'completed': 'success',
        'in_progress': 'info',
        'pending': 'warning',
        'cancelled': 'danger',
        'delayed': 'danger',
    };
    return statusMap[status] || 'secondary';
}

/**
 * Initialize charts
 */
function initCharts(stats) {
    // Trip Status Chart
    const tripStatusCtx = document.getElementById('tripStatusChart');
    if (tripStatusCtx) {
        new Chart(tripStatusCtx, {
            type: 'doughnut',
            data: {
                labels: ['Active', 'Completed', 'Pending'],
                datasets: [{
                    data: [
                        stats.trips.active,
                        stats.trips.completed,
                        stats.trips.total - stats.trips.active - stats.trips.completed
                    ],
                    backgroundColor: ['#3498db', '#27ae60', '#f39c12'],
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom',
                    }
                }
            }
        });
    }

    // Expenses Chart
    const expensesCtx = document.getElementById('expensesChart');
    if (expensesCtx) {
        new Chart(expensesCtx, {
            type: 'bar',
            data: {
                labels: ['Fuel', 'Maintenance', 'Total'],
                datasets: [{
                    label: 'Expenses ($)',
                    data: [
                        stats.fuel.total_cost,
                        stats.maintenance.total_cost,
                        stats.fuel.total_cost + stats.maintenance.total_cost
                    ],
                    backgroundColor: ['#3498db', '#e74c3c', '#95a5a6'],
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                    }
                },
                plugins: {
                    legend: {
                        display: false,
                    }
                }
            }
        });
    }
}

/**
 * View trip details
 */
function viewTrip(tripId) {
    // Redirect to trip details page
    window.location.href = `/pages/trip-details.html?id=${tripId}`;
}

/**
 * Logout
 */
document.getElementById('logout-btn')?.addEventListener('click', (e) => {
    e.preventDefault();
    apiClient.logout();
    window.location.href = '/pages/login.html';
});
