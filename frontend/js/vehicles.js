/**
 * Vehicles Management JavaScript
 */

document.addEventListener('DOMContentLoaded', async () => {
    // Check authentication
    if (!localStorage.getItem('access_token')) {
        window.location.href = '/pages/login.html';
        return;
    }

    document.querySelectorAll('.vehicle-tab').forEach(tab => {
        tab.addEventListener('click', () => setVehicleView(tab.dataset.view));
    });
    document.getElementById('vehicle-search')?.addEventListener('input', renderVehicles);
    document.getElementById('inventory-type-filter')?.addEventListener('change', renderVehicles);
    document.getElementById('inventory-status-filter')?.addEventListener('change', renderVehicles);
    document.getElementById('export-vehicles')?.addEventListener('click', exportVehicles);
    document.getElementById('toggle-sidebar')?.addEventListener('click', () => document.querySelector('.sidebar').classList.toggle('active'));
    document.getElementById('logout-btn')?.addEventListener('click', event => {
        event.preventDefault();
        apiClient.logout();
        window.location.href = '/pages/login.html';
    });

    await loadVehicles();

    // Add event listener for form submission
    document.getElementById('addVehicleForm')?.addEventListener('submit', addVehicle);
    document.getElementById('addVehicleModal')?.addEventListener('hidden.bs.modal', resetVehicleForm);
});

let vehicles = [];
let editingVehicleId = null;

/**
 * Load all vehicles
 */
async function loadVehicles() {
    try {
        const response = await apiClient.getVehicles({ limit: 100 });
        vehicles = Array.isArray(response) ? response : (response.results || []);
        populateVehicleTypeFilter();
        renderVehicles();
    } catch (error) {
        console.error('Failed to load vehicles:', error);
        document.getElementById('vehicles-table').innerHTML = '<tr><td colspan="7" class="text-center">Could not load vehicles. Refresh the page to try again.</td></tr>';
        document.getElementById('vehicle-health-table').innerHTML = '<tr><td colspan="6" class="text-center">Could not load vehicle health.</td></tr>';
    }
}

function renderVehicles() {
    const query = (document.getElementById('vehicle-search')?.value || '').trim().toLowerCase();
    const type = document.getElementById('inventory-type-filter')?.value || 'all';
    const status = document.getElementById('inventory-status-filter')?.value || 'all';
    const filtered = vehicles.filter(vehicle => {
        const searchable = [vehicle.vehicle_number, vehicle.vehicle_type, vehicle.registration_number, vehicle.current_location, vehicle.status]
            .filter(Boolean).join(' ').toLowerCase();
        return (!query || searchable.includes(query))
            && (type === 'all' || vehicle.vehicle_type === type)
            && (status === 'all' || vehicle.status === status);
    });
    renderInventory(filtered);
    renderHealth(filtered);
    renderSummary();
    document.getElementById('inventory-result-count').textContent = `${filtered.length} of ${vehicles.length} vehicles`;
}

function renderInventory(items) {
    const tbody = document.getElementById('vehicles-table');
    if (!items.length) {
        tbody.innerHTML = `<tr><td colspan="7" class="text-center">${vehicles.length ? 'No vehicles match these filters.' : 'No vehicles in your fleet yet.'}</td></tr>`;
        return;
    }
    tbody.innerHTML = items.map(vehicle => `
        <tr>
            <td><strong>${escapeHtml(vehicle.vehicle_number)}</strong></td>
            <td>${escapeHtml(vehicle.vehicle_type)}</td>
            <td>${escapeHtml(vehicle.registration_number)}</td>
            <td><span class="badge badge-${getVehicleStatusClass(vehicle.status)}">${escapeHtml(formatLabel(vehicle.status))}</span></td>
            <td>${escapeHtml(vehicle.current_location || 'Not recorded')}</td>
            <td>${formatDistance(vehicle.total_distance)}</td>
            <td class="vehicle-actions">
                <button class="btn btn-sm btn-light" type="button" onclick="editVehicle(${Number(vehicle.id)})" aria-label="Edit ${escapeHtml(vehicle.vehicle_number)}" title="Edit vehicle"><i class="fas fa-pen" aria-hidden="true"></i></button>
                <button class="btn btn-sm btn-light text-danger" type="button" onclick="deleteVehicle(${Number(vehicle.id)})" aria-label="Delete ${escapeHtml(vehicle.vehicle_number)}" title="Delete vehicle"><i class="fas fa-trash" aria-hidden="true"></i></button>
            </td>
        </tr>
    `).join('');
}

function renderHealth(items) {
    const signals = items.map(getVehicleHealth);
    const healthy = signals.filter(signal => signal.level === 'healthy').length;
    const attention = signals.filter(signal => signal.level === 'attention').length;
    const watch = signals.filter(signal => signal.level === 'watch').length;
    document.getElementById('health-summary').innerHTML = `
        <div><strong>${healthy}</strong><span>Clear</span></div>
        <div><strong>${watch}</strong><span>Due soon</span></div>
        <div><strong>${attention}</strong><span>Needs attention</span></div>
    `;
    const tbody = document.getElementById('vehicle-health-table');
    if (!items.length) {
        tbody.innerHTML = '<tr><td colspan="6" class="text-center">No vehicles match these filters.</td></tr>';
        return;
    }
    tbody.innerHTML = items.map((vehicle, index) => {
        const signal = signals[index];
        return `
            <tr>
                <td><strong>${escapeHtml(vehicle.vehicle_number)}</strong><small class="vehicle-subline">${escapeHtml(vehicle.vehicle_type)} · ${escapeHtml(vehicle.registration_number)}</small></td>
                <td><span class="badge badge-${getVehicleStatusClass(vehicle.status)}">${escapeHtml(formatLabel(vehicle.status))}</span></td>
                <td>${formatDocumentDate(vehicle.insurance_expiry)}</td>
                <td>${formatDocumentDate(vehicle.registration_expiry)}</td>
                <td>${formatDistance(vehicle.total_distance)}</td>
                <td><span class="health-indicator health-${signal.level}"><i class="fas ${signal.icon}" aria-hidden="true"></i>${escapeHtml(signal.label)}</span><small class="vehicle-subline">${escapeHtml(signal.detail)}</small></td>
            </tr>
        `;
    }).join('');
}

function renderSummary() {
    document.getElementById('vehicle-count-total').textContent = vehicles.length;
    document.getElementById('vehicle-count-active').textContent = vehicles.filter(vehicle => vehicle.status === 'active').length;
    document.getElementById('vehicle-count-maintenance').textContent = vehicles.filter(vehicle => vehicle.status === 'maintenance').length;
    document.getElementById('vehicle-count-attention').textContent = vehicles.filter(vehicle => getVehicleHealth(vehicle).level !== 'healthy').length;
}

function getVehicleHealth(vehicle) {
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    const issues = [];
    const dueSoon = [];
    for (const [field, label] of [['insurance_expiry', 'Insurance'], ['registration_expiry', 'Registration']]) {
        if (!vehicle[field]) continue;
        const expiry = new Date(`${vehicle[field]}T00:00:00`);
        const daysRemaining = Math.ceil((expiry - today) / 86400000);
        if (daysRemaining < 0) issues.push(`${label} expired`);
        else if (daysRemaining <= 30) dueSoon.push(`${label} due in ${daysRemaining} days`);
    }
    if (vehicle.status !== 'active') issues.unshift(`Status: ${formatLabel(vehicle.status || 'unknown')}`);
    if (issues.length) return { level: 'attention', label: 'Needs attention', detail: issues.join(' · '), icon: 'fa-triangle-exclamation' };
    if (dueSoon.length) return { level: 'watch', label: 'Due soon', detail: dueSoon.join(' · '), icon: 'fa-clock' };
    return { level: 'healthy', label: 'Clear', detail: 'No recorded issues', icon: 'fa-circle-check' };
}

function formatDocumentDate(dateValue) {
    if (!dateValue) return '<span class="text-muted">Not recorded</span>';
    const expiry = new Date(`${dateValue}T00:00:00`);
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    const daysRemaining = Math.ceil((expiry - today) / 86400000);
    const date = escapeHtml(expiry.toLocaleDateString());
    if (daysRemaining < 0) return `<span class="document-expired">${date} · Expired</span>`;
    if (daysRemaining <= 30) return `<span class="document-due">${date} · Due soon</span>`;
    return date;
}

function populateVehicleTypeFilter() {
    const select = document.getElementById('inventory-type-filter');
    const currentValue = select.value;
    const types = [...new Set(vehicles.map(vehicle => vehicle.vehicle_type).filter(Boolean))].sort();
    select.innerHTML = '<option value="all">All types</option>' + types.map(type => `<option value="${escapeHtml(type)}">${escapeHtml(formatLabel(type))}</option>`).join('');
    if (types.includes(currentValue)) select.value = currentValue;
}

function setVehicleView(view) {
    const showHealth = view === 'health';
    document.getElementById('inventory-panel').hidden = showHealth;
    document.getElementById('health-panel').hidden = !showHealth;
    document.querySelectorAll('.vehicle-tab').forEach(tab => {
        const selected = tab.dataset.view === view;
        tab.classList.toggle('active', selected);
        tab.setAttribute('aria-selected', String(selected));
    });
}

function exportVehicles() {
    const query = (document.getElementById('vehicle-search')?.value || '').trim().toLowerCase();
    const type = document.getElementById('inventory-type-filter')?.value || 'all';
    const status = document.getElementById('inventory-status-filter')?.value || 'all';
    const rows = vehicles.filter(vehicle => {
        const searchable = [vehicle.vehicle_number, vehicle.vehicle_type, vehicle.registration_number, vehicle.current_location, vehicle.status]
            .filter(Boolean).join(' ').toLowerCase();
        return (!query || searchable.includes(query)) && (type === 'all' || vehicle.vehicle_type === type) && (status === 'all' || vehicle.status === status);
    });
    const columns = ['vehicle_number', 'vehicle_type', 'registration_number', 'status', 'current_location', 'total_distance', 'insurance_expiry', 'registration_expiry'];
    const csv = [columns.join(','), ...rows.map(vehicle => columns.map(column => csvValue(vehicle[column])).join(','))].join('\r\n');
    const link = document.createElement('a');
    link.href = URL.createObjectURL(new Blob([csv], { type: 'text/csv;charset=utf-8' }));
    link.download = 'vehicle-inventory.csv';
    link.click();
    URL.revokeObjectURL(link.href);
}

function csvValue(value) {
    return `"${String(value ?? '').replaceAll('"', '""')}"`;
}

function escapeHtml(value) {
    return String(value ?? '').replace(/[&<>"']/g, character => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[character]);
}

function formatLabel(value) {
    return String(value || 'unknown').replaceAll('_', ' ').replace(/\b\w/g, character => character.toUpperCase());
}

function formatDistance(value) {
    const distance = Number(value);
    return Number.isFinite(distance) ? `${distance.toLocaleString()} km` : 'Not recorded';
}

/**
 * Get vehicle status badge class
 */
function getVehicleStatusClass(status) {
    const statusMap = {
        'active': 'success',
        'maintenance': 'warning',
        'inactive': 'secondary',
        'retired': 'danger',
    };
    return statusMap[status] || 'secondary';
}

/**
 * Add new vehicle
 */
async function addVehicle(e) {
    e?.preventDefault();

    const vehicleData = {
        vehicle_number: document.getElementById('vehicleNumber').value,
        vehicle_type: document.getElementById('vehicleType').value,
        registration_number: document.getElementById('registrationNumber').value,
        purchase_date: document.getElementById('purchaseDate').value,
        status: document.getElementById('vehicleStatus').value,
        insurance_expiry: document.getElementById('insuranceExpiry').value || null,
        registration_expiry: document.getElementById('registrationExpiry').value || null,
        current_location: document.getElementById('currentLocation').value,
        total_distance: Number(document.getElementById('totalDistance').value || 0),
        latitude: document.getElementById('vehicleLatitude').value === '' ? null : Number(document.getElementById('vehicleLatitude').value),
        longitude: document.getElementById('vehicleLongitude').value === '' ? null : Number(document.getElementById('vehicleLongitude').value),
    };

    try {
        if (editingVehicleId) {
            await apiClient.updateVehicle(editingVehicleId, vehicleData);
        } else {
            await apiClient.createVehicle(vehicleData);
        }
        const modal = bootstrap.Modal.getInstance(document.getElementById('addVehicleModal'));
        modal?.hide();
        alert(editingVehicleId ? 'Vehicle updated successfully' : 'Vehicle added successfully');
        await loadVehicles();
    } catch (error) {
        console.error('Failed to add vehicle:', error);
        alert('Failed to add vehicle');
    }
}

/**
 * Edit vehicle
 */
async function editVehicle(vehicleId) {
    const vehicle = vehicles.find(item => item.id === vehicleId);
    if (!vehicle) return;

    editingVehicleId = vehicle.id;
    document.getElementById('vehicleNumber').value = vehicle.vehicle_number;
    document.getElementById('vehicleType').value = vehicle.vehicle_type.toLowerCase();
    document.getElementById('registrationNumber').value = vehicle.registration_number;
    document.getElementById('purchaseDate').value = vehicle.purchase_date;
    document.getElementById('vehicleStatus').value = vehicle.status;
    document.getElementById('insuranceExpiry').value = vehicle.insurance_expiry || '';
    document.getElementById('registrationExpiry').value = vehicle.registration_expiry || '';
    document.getElementById('currentLocation').value = vehicle.current_location || '';
    document.getElementById('totalDistance').value = vehicle.total_distance || 0;
    document.getElementById('vehicleLatitude').value = vehicle.latitude ?? '';
    document.getElementById('vehicleLongitude').value = vehicle.longitude ?? '';
    document.querySelector('#addVehicleModal .modal-title').textContent = 'Edit Vehicle';
    document.getElementById('save-vehicle-button').textContent = 'Save changes';
    bootstrap.Modal.getOrCreateInstance(document.getElementById('addVehicleModal')).show();
}

function resetVehicleForm() {
    editingVehicleId = null;
    document.getElementById('addVehicleForm').reset();
    document.querySelector('#addVehicleModal .modal-title').textContent = 'Add New Vehicle';
    document.getElementById('save-vehicle-button').textContent = 'Add Vehicle';
}

/**
 * Delete vehicle
 */
async function deleteVehicle(vehicleId) {
    if (!confirm('Are you sure you want to delete this vehicle?')) {
        return;
    }

    try {
        await apiClient.deleteVehicle(vehicleId);
        alert('Vehicle deleted successfully');
        await loadVehicles();
    } catch (error) {
        console.error('Failed to delete vehicle:', error);
        alert('Failed to delete vehicle');
    }
}
