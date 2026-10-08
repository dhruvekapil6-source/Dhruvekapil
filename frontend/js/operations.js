const operationsConfig = {
    drivers: {
        title: 'Drivers', endpoint: '/drivers/',
        description: 'Driver records. Link an existing account by user ID.',
        fields: [
            ['user', 'User ID', 'number'], ['driver_id', 'Driver ID'], ['license_number', 'License number'],
            ['license_class', 'License class', 'select', ['A', 'B', 'C', 'D', 'LMV']], ['license_expiry', 'License expiry', 'date'],
            ['phone', 'Phone'], ['address', 'Address', 'textarea'], ['city', 'City'], ['state', 'State'], ['country', 'Country'],
            ['postal_code', 'Postal code'], ['experience_years', 'Years of experience', 'number'], ['date_of_birth', 'Date of birth', 'date'],
            ['assigned_vehicle', 'Assigned vehicle ID', 'number'], ['status', 'Status', 'select', ['active', 'inactive', 'on_leave']],
        ], columns: ['driver_id', 'user', 'license_number', 'license_expiry', 'status'],
    },
    trips: {
        title: 'Trips', endpoint: '/trips/', description: 'Plan and track scheduled fleet trips.',
        fields: [
            ['trip_id', 'Trip ID'], ['driver', 'Driver ID', 'number'], ['vehicle', 'Vehicle ID', 'number'],
            ['pickup_location', 'Pickup location'], ['pickup_latitude', 'Pickup latitude', 'number'], ['pickup_longitude', 'Pickup longitude', 'number'],
            ['destination_location', 'Destination'], ['destination_latitude', 'Destination latitude', 'number'], ['destination_longitude', 'Destination longitude', 'number'],
            ['distance', 'Distance (km)', 'number'], ['estimated_time', 'Estimated time (minutes)', 'number'],
            ['status', 'Status', 'select', ['pending', 'assigned', 'in_progress', 'completed', 'cancelled', 'delayed']],
            ['scheduled_date', 'Scheduled date', 'date'], ['scheduled_time', 'Scheduled time', 'time'], ['notes', 'Notes', 'textarea'],
        ], columns: ['trip_id', 'driver', 'vehicle', 'scheduled_date', 'status'],
    },
    routes: {
        title: 'Routes', endpoint: '/routes/', description: 'Store route plans and recorded distance/cost estimates. Route optimization is not calculated automatically.',
        fields: [
            ['route_id', 'Route ID'], ['vehicle', 'Vehicle ID', 'number'], ['algorithm_used', 'Algorithm label', 'select', ['dijkstra', 'astar', 'networkx', 'ortools']],
            ['delivery_points', 'Delivery points (JSON)', 'json'], ['optimized_sequence', 'Sequence (JSON)', 'json'],
            ['total_distance', 'Total distance (km)', 'number'], ['estimated_time', 'Estimated time (minutes)', 'number'],
            ['estimated_fuel', 'Estimated fuel (liters)', 'number'], ['estimated_cost', 'Estimated cost', 'number'],
            ['status', 'Status', 'select', ['pending', 'active', 'completed']],
        ], columns: ['route_id', 'vehicle', 'algorithm_used', 'total_distance', 'status'],
    },
    fuel: {
        title: 'Fuel', endpoint: '/fuel/entries/', description: 'Record fuel purchases, odometer readings, and costs.',
        fields: [
            ['vehicle', 'Vehicle ID', 'number'], ['driver', 'Driver ID (optional)', 'number'], ['date', 'Date', 'date'],
            ['amount', 'Amount (liters)', 'number'], ['cost', 'Cost', 'number'], ['mileage', 'Odometer (km)', 'number'],
            ['fuel_station', 'Fuel station'], ['notes', 'Notes', 'textarea'],
        ], columns: ['date', 'vehicle', 'driver', 'amount', 'cost', 'mileage'],
    },
    maintenance: {
        title: 'Maintenance', endpoint: '/maintenance/records/', description: 'Track vehicle service records and completion status.',
        fields: [
            ['vehicle', 'Vehicle ID', 'number'], ['maintenance_type', 'Type', 'select', ['routine', 'repair', 'inspection', 'replacement', 'other']],
            ['description', 'Description', 'textarea'], ['service_provider', 'Service provider'], ['cost', 'Total cost', 'number'],
            ['service_date', 'Service date', 'date'], ['completion_date', 'Completion date', 'date'], ['odometer_reading', 'Odometer (km)', 'number'],
            ['status', 'Status', 'select', ['pending', 'in_progress', 'completed']],
        ], columns: ['vehicle', 'maintenance_type', 'service_date', 'cost', 'status'],
    },
    reports: {
        title: 'Reports', endpoint: '/reports/', description: 'Create report requests. File generation and downloads are not configured yet.',
        fields: [
            ['report_type', 'Report type', 'select', ['vehicle', 'driver', 'fuel', 'trip', 'maintenance', 'financial']],
            ['format', 'Format', 'select', ['pdf', 'excel', 'csv']], ['title', 'Title'], ['description', 'Description', 'textarea'],
            ['start_date', 'Start date', 'date'], ['end_date', 'End date', 'date'], ['generated_by', 'Requested by'],
        ], columns: ['title', 'report_type', 'format', 'start_date', 'end_date', 'status'],
    },
    notifications: {
        title: 'Notifications', endpoint: '/notifications/', description: 'Manage in-app notification records.',
        fields: [
            ['user', 'User ID', 'number'], ['notification_type', 'Type', 'select', ['service_due', 'insurance_expiry', 'license_expiry', 'trip_delay', 'fuel_low', 'maintenance_reminder', 'system_alert']],
            ['title', 'Title'], ['message', 'Message', 'textarea'], ['related_object_id', 'Related record ID', 'number'], ['related_object_type', 'Related record type'],
            ['is_read', 'Read', 'checkbox'],
        ], columns: ['user', 'notification_type', 'title', 'is_read', 'created_at'],
    },
    profile: {
        title: 'Profile', endpoint: '/users/me/', description: 'View your account details and update contact information.', profile: true,
        fields: [['phone', 'Phone'], ['address', 'Address', 'textarea'], ['city', 'City'], ['state', 'State'], ['country', 'Country'], ['postal_code', 'Postal code']],
        columns: ['username', 'email', 'role', 'phone', 'city', 'country'],
    },
};

const moduleName = document.body.dataset.module;
const config = moduleName === 'trip-details'
    ? { ...operationsConfig.trips, title: 'Trip details', detail: true }
    : operationsConfig[moduleName];
const formPanel = document.getElementById('record-form-panel');
const recordForm = document.getElementById('record-form');
const fieldsContainer = document.getElementById('record-fields');
const pageMessage = document.getElementById('page-message');
let records = [];
let editingId = null;
let profileRecord = null;

document.addEventListener('DOMContentLoaded', async () => {
    if (!localStorage.getItem('access_token')) {
        window.location.href = '/pages/login.html';
        return;
    }
    if (!config) {
        showMessage('This operations page is not configured.', 'danger');
        return;
    }
    document.title = `${config.title} - Fleet Manager`;
    document.getElementById('page-title').textContent = config.title;
    document.getElementById('page-heading').textContent = config.title;
    document.getElementById('page-description').textContent = config.description;
    document.getElementById('new-record').hidden = Boolean(config.profile);
    document.getElementById('new-record').addEventListener('click', () => openForm());
    document.getElementById('close-form').addEventListener('click', closeForm);
    document.getElementById('cancel-form').addEventListener('click', closeForm);
    document.getElementById('refresh-records').addEventListener('click', loadRecords);
    document.getElementById('toggle-sidebar').addEventListener('click', () => document.querySelector('.sidebar').classList.toggle('active'));
    document.getElementById('logout-btn').addEventListener('click', event => {
        event.preventDefault();
        apiClient.logout();
        window.location.href = '/pages/login.html';
    });
    recordForm.addEventListener('submit', saveRecord);
    renderTableHead();
    await loadRecords();
});

function renderTableHead() {
    document.getElementById('records-head').innerHTML = `<tr>${config.columns.map(column => `<th>${escapeHtml(formatLabel(column))}</th>`).join('')}${config.profile ? '' : '<th>Actions</th>'}</tr>`;
}

async function loadRecords() {
    const body = document.getElementById('records-body');
    body.innerHTML = `<tr><td colspan="${config.columns.length + 1}">Loading...</td></tr>`;
    try {
        if (config.profile) {
            profileRecord = await apiClient.get(config.endpoint);
            records = [profileRecord];
            document.getElementById('user-name').textContent = profileRecord.user?.username || 'Profile';
            renderFormFields(profileRecord);
            fieldsContainer.querySelectorAll('input, textarea').forEach(field => {
                if (field.name === 'role') field.disabled = true;
            });
        } else if (config.detail) {
            const tripId = new URLSearchParams(window.location.search).get('id');
            if (!tripId) throw new Error('Select a trip from the dashboard first.');
            records = [await apiClient.get(`${config.endpoint}${encodeURIComponent(tripId)}/`)];
            document.getElementById('new-record').hidden = true;
        } else {
            const response = await apiClient.get(config.endpoint, { limit: 100 });
            records = Array.isArray(response) ? response : (response.results || []);
        }
        renderRows();
        clearMessage();
    } catch (error) {
        body.innerHTML = `<tr><td colspan="${config.columns.length + 1}">Could not load records: ${escapeHtml(error.message)}</td></tr>`;
        showMessage(error.message, 'danger');
    }
}

function renderRows() {
    const body = document.getElementById('records-body');
    if (!records.length) {
        body.innerHTML = `<tr><td colspan="${config.columns.length + 1}">No ${escapeHtml(config.title.toLowerCase())} records yet.</td></tr>`;
        return;
    }
    body.innerHTML = records.map(record => `<tr>${config.columns.map(column => {
        const value = column === 'username' ? record.user?.username : record[column];
        const shown = value && typeof value === 'object' ? JSON.stringify(value) : value;
        return `<td>${escapeHtml(shown ?? '—')}</td>`;
    }).join('')}${config.profile ? '' : `<td class="text-nowrap"><button class="btn btn-sm btn-light" type="button" data-edit="${Number(record.id)}" aria-label="Edit record"><i class="fas fa-pen"></i></button> <button class="btn btn-sm btn-light text-danger" type="button" data-delete="${Number(record.id)}" aria-label="Delete record"><i class="fas fa-trash"></i></button></td>`}</tr>`).join('');
    body.querySelectorAll('[data-edit]').forEach(button => button.addEventListener('click', () => openForm(records.find(item => item.id === Number(button.dataset.edit)))));
    body.querySelectorAll('[data-delete]').forEach(button => button.addEventListener('click', () => deleteRecord(Number(button.dataset.delete))));
}

function renderFormFields(record = {}) {
    fieldsContainer.innerHTML = config.fields.map(([name, label, type = 'text', options]) => {
        const value = record[name] ?? '';
        const columnClass = type === 'textarea' || type === 'json' ? 'col-12' : 'col-md-6';
        let control;
        if (type === 'select') {
            control = `<select class="form-select" name="${name}" ${record.id ? '' : 'required'}>${options.map(option => `<option value="${escapeHtml(option)}" ${String(value) === option ? 'selected' : ''}>${escapeHtml(formatLabel(option))}</option>`).join('')}</select>`;
        } else if (type === 'textarea' || type === 'json') {
            const formatted = type === 'json' ? JSON.stringify(value || [], null, 2) : value;
            control = `<textarea class="form-control" name="${name}" rows="${type === 'json' ? 4 : 2}" ${type === 'json' ? 'data-json' : ''}>${escapeHtml(formatted)}</textarea>`;
        } else if (type === 'checkbox') {
            control = `<input class="form-check-input" type="checkbox" name="${name}" ${value ? 'checked' : ''}>`;
        } else {
            control = `<input class="form-control" type="${type}" name="${name}" value="${escapeHtml(value)}" ${type === 'number' ? 'step="any"' : ''} ${record.id ? '' : 'required'}>`;
        }
        return `<div class="${columnClass}"><label class="form-label">${escapeHtml(label)}${type === 'json' ? ' (valid JSON)' : ''}</label>${control}</div>`;
    }).join('');
}

function openForm(record = null) {
    editingId = record?.id ?? null;
    document.getElementById('form-heading').textContent = editingId ? `Edit ${config.title.toLowerCase()}` : `New ${config.title.toLowerCase()} record`;
    renderFormFields(record || {});
    formPanel.hidden = false;
    formPanel.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function closeForm() {
    formPanel.hidden = true;
    editingId = null;
    recordForm.reset();
}

async function saveRecord(event) {
    event.preventDefault();
    const payload = {};
    for (const field of fieldsContainer.querySelectorAll('[name]')) {
        if (field.disabled) continue;
        if (field.dataset.json !== undefined) {
            try {
                payload[field.name] = JSON.parse(field.value);
            } catch {
                showMessage(`${field.name} must contain valid JSON.`, 'danger');
                return;
            }
        } else if (field.type === 'checkbox') {
            payload[field.name] = field.checked;
        } else if (field.value !== '') {
            payload[field.name] = field.value;
        }
    }
    try {
        if (config.profile) {
            await apiClient.patch(`/users/profiles/${profileRecord.id}/`, payload);
        } else if (editingId) {
            await apiClient.put(`${config.endpoint}${editingId}/`, payload);
        } else {
            await apiClient.post(config.endpoint, payload);
        }
        closeForm();
        showMessage('Record saved.', 'success');
        await loadRecords();
    } catch (error) {
        showMessage(error.message, 'danger');
    }
}

async function deleteRecord(id) {
    if (!window.confirm('Delete this record?')) return;
    try {
        await apiClient.delete(`${config.endpoint}${id}/`);
        showMessage('Record deleted.', 'success');
        await loadRecords();
    } catch (error) {
        showMessage(error.message, 'danger');
    }
}

function showMessage(message, type) {
    pageMessage.textContent = message;
    pageMessage.className = `alert alert-${type}`;
}

function clearMessage() {
    pageMessage.textContent = '';
    pageMessage.className = 'alert d-none';
}

function formatLabel(value) {
    return String(value).replaceAll('_', ' ').replace(/\b\w/g, character => character.toUpperCase());
}

function escapeHtml(value) {
    return String(value ?? '').replace(/[&<>"']/g, character => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[character]));
}