// Watchlist CRUD operations
const API_URL = '/api/watchlist';

async function loadWatchlist() {
    const activeOnly = document.getElementById('activeOnlyToggle').checked;
    const res = await fetch(`${API_URL}/?active_only=${activeOnly}`);
    const json = await res.json();
    renderWatchlist(json.data);
}

function renderWatchlist(items) {
    const tbody = document.getElementById('watchlistBody');
    const empty = document.getElementById('watchlistEmpty');

    if (items.length === 0) {
        tbody.innerHTML = '';
        empty.classList.remove('d-none');
        return;
    }

    empty.classList.add('d-none');
    tbody.innerHTML = items.map(item => `
        <tr data-testid="watchlist-row-${item.id}">
            <td data-testid="watchlist-symbol-${item.id}">
                <strong>${item.symbol}</strong>
            </td>
            <td>${item.target_price ? '$' + item.target_price.toFixed(2) : '-'}</td>
            <td>${item.sector || '-'}</td>
            <td>${item.notes || '-'}</td>
            <td>${new Date(item.added_date).toLocaleDateString()}</td>
            <td>
                <span class="badge ${item.is_active ? 'bg-success' : 'bg-secondary'}">
                    ${item.is_active ? 'Active' : 'Inactive'}
                </span>
            </td>
            <td>
                <button class="btn btn-sm btn-outline-primary me-1" data-testid="watchlist-edit-${item.id}"
                        onclick="openEdit(${item.id}, '${item.symbol}', ${item.target_price || 'null'}, '${item.sector || ''}', '${(item.notes || '').replace(/'/g, "\\'")}', ${item.is_active})">
                    Edit
                </button>
                <button class="btn btn-sm btn-outline-danger" data-testid="watchlist-delete-${item.id}"
                        onclick="deleteItem(${item.id}, '${item.symbol}')">
                    Delete
                </button>
            </td>
        </tr>
    `).join('');
}

// Add new item
document.getElementById('addWatchlistForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const body = {
        symbol: document.getElementById('symbolInput').value,
        target_price: parseFloat(document.getElementById('targetPriceInput').value) || null,
        sector: document.getElementById('sectorInput').value || null,
        notes: document.getElementById('notesInput').value || null
    };

    const res = await fetch(API_URL + '/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
    });
    const json = await res.json();

    if (res.ok) {
        showFlash(json.message, 'success');
        e.target.reset();
        loadWatchlist();
    } else {
        showFlash(json.message, 'danger');
    }
});

// Edit modal
function openEdit(id, symbol, targetPrice, sector, notes, isActive) {
    document.getElementById('editId').value = id;
    document.getElementById('editSymbol').value = symbol;
    document.getElementById('editTargetPrice').value = targetPrice || '';
    document.getElementById('editSector').value = sector;
    document.getElementById('editNotes').value = notes;
    document.getElementById('editActive').checked = isActive;
    new bootstrap.Modal(document.getElementById('editModal')).show();
}

document.getElementById('editSaveBtn').addEventListener('click', async () => {
    const id = document.getElementById('editId').value;
    const body = {
        target_price: parseFloat(document.getElementById('editTargetPrice').value) || null,
        sector: document.getElementById('editSector').value || null,
        notes: document.getElementById('editNotes').value || null,
        is_active: document.getElementById('editActive').checked
    };

    const res = await fetch(`${API_URL}/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
    });
    const json = await res.json();

    if (res.ok) {
        showFlash(json.message, 'success');
        bootstrap.Modal.getInstance(document.getElementById('editModal')).hide();
        loadWatchlist();
    } else {
        showFlash(json.message, 'danger');
    }
});

// Delete
async function deleteItem(id, symbol) {
    if (!confirm(`Remove ${symbol} from watchlist?`)) return;

    const res = await fetch(`${API_URL}/${id}`, { method: 'DELETE' });
    const json = await res.json();

    if (res.ok) {
        showFlash(json.message, 'success');
        loadWatchlist();
    } else {
        showFlash(json.message, 'danger');
    }
}

// Flash messages
function showFlash(message, type) {
    const container = document.getElementById('flash-messages');
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} alert-dismissible fade show`;
    alert.innerHTML = `${message}<button type="button" class="btn-close" data-bs-dismiss="alert"></button>`;
    container.appendChild(alert);
    setTimeout(() => alert.remove(), 3000);
}

// Filter toggle
document.getElementById('activeOnlyToggle').addEventListener('change', loadWatchlist);

// Load on page ready
loadWatchlist();
