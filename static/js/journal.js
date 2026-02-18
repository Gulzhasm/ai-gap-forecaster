// Trade Journal CRUD
const API_URL = '/api/trades';

async function loadTrades() {
    const status = document.getElementById('statusFilter').value;
    const symbol = document.getElementById('symbolFilter').value.trim();
    let url = `${API_URL}/?status=${status}`;
    if (symbol) url += `&symbol=${symbol}`;

    const res = await fetch(url);
    const json = await res.json();
    renderTrades(json.data.trades);
}

function renderTrades(trades) {
    const tbody = document.getElementById('tradesBody');
    const empty = document.getElementById('tradesEmpty');

    if (trades.length === 0) {
        tbody.innerHTML = '';
        empty.classList.remove('d-none');
        return;
    }

    empty.classList.add('d-none');
    tbody.innerHTML = trades.map(t => {
        const pnlClass = t.pnl > 0 ? 'pnl-positive' : t.pnl < 0 ? 'pnl-negative' : '';
        const pnlText = t.pnl !== null ? `$${t.pnl.toFixed(2)}` : '-';
        const gapClass = t.gap_type === 'gap_up' ? 'gap-up' : 'gap-down';
        const gapArrow = t.gap_type === 'gap_up' ? '&#9650;' : '&#9660;';
        const stars = t.setup_rating ? '&#9733;'.repeat(t.setup_rating) : '-';

        return `
        <tr data-testid="trade-row-${t.id}">
            <td><strong>${t.symbol}</strong></td>
            <td><span class="badge ${t.direction === 'long' ? 'bg-success' : 'bg-danger'}">${t.direction}</span></td>
            <td class="${gapClass}" data-testid="trade-gap-${t.id}">${gapArrow} ${t.gap_percent ? t.gap_percent.toFixed(1) + '%' : '-'}</td>
            <td>$${t.entry_price.toFixed(2)}</td>
            <td>${t.exit_price ? '$' + t.exit_price.toFixed(2) : '-'}</td>
            <td>${t.quantity}</td>
            <td class="${pnlClass}" data-testid="trade-pnl-${t.id}">${pnlText}</td>
            <td>
                <span class="badge ${t.status === 'open' ? 'bg-primary' : t.status === 'closed' ? 'bg-secondary' : 'bg-warning'}">
                    ${t.status}
                </span>
            </td>
            <td>${stars}</td>
            <td>${new Date(t.entry_date).toLocaleDateString()}</td>
            <td>
                ${t.status === 'open' ? `
                    <button class="btn btn-sm btn-outline-success me-1" data-testid="trade-close-${t.id}"
                            onclick="openCloseTrade(${t.id}, '${t.symbol}')">Close</button>
                ` : ''}
                <button class="btn btn-sm btn-outline-danger" data-testid="trade-delete-${t.id}"
                        onclick="deleteTrade(${t.id})">Del</button>
            </td>
        </tr>`;
    }).join('');
}

function resetTradeForm() {
    document.getElementById('tradeForm').reset();
    document.getElementById('tradeModalTitle').textContent = 'New Trade';
}

// Save new trade
document.getElementById('tradeSaveBtn').addEventListener('click', async () => {
    const body = {
        symbol: document.getElementById('tradeSymbol').value,
        direction: document.getElementById('tradeDirection').value,
        gap_type: document.getElementById('tradeGapType').value,
        entry_price: parseFloat(document.getElementById('tradeEntryPrice').value),
        quantity: parseInt(document.getElementById('tradeQuantity').value),
        gap_percent: parseFloat(document.getElementById('tradeGapPercent').value) || null,
        setup_rating: parseInt(document.getElementById('tradeRating').value) || null,
        notes: document.getElementById('tradeNotes').value || null
    };

    const res = await fetch(API_URL + '/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
    });
    const json = await res.json();

    if (res.ok) {
        showFlash(json.message, 'success');
        bootstrap.Modal.getInstance(document.getElementById('tradeModal')).hide();
        loadTrades();
    } else {
        showFlash(json.message, 'danger');
    }
});

// Close trade
function openCloseTrade(id, symbol) {
    document.getElementById('closeTradeId').value = id;
    document.getElementById('closeTradeSymbol').textContent = symbol;
    document.getElementById('closeTradeExitPrice').value = '';
    new bootstrap.Modal(document.getElementById('closeTradeModal')).show();
}

document.getElementById('closeTradeBtn').addEventListener('click', async () => {
    const id = document.getElementById('closeTradeId').value;
    const exitPrice = parseFloat(document.getElementById('closeTradeExitPrice').value);
    if (!exitPrice || exitPrice <= 0) {
        showFlash('Exit price must be positive', 'danger');
        return;
    }

    const res = await fetch(`${API_URL}/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ exit_price: exitPrice })
    });
    const json = await res.json();

    if (res.ok) {
        showFlash(json.message, 'success');
        bootstrap.Modal.getInstance(document.getElementById('closeTradeModal')).hide();
        loadTrades();
    } else {
        showFlash(json.message, 'danger');
    }
});

// Delete trade
async function deleteTrade(id) {
    if (!confirm('Delete this trade?')) return;

    const res = await fetch(`${API_URL}/${id}`, { method: 'DELETE' });
    const json = await res.json();

    if (res.ok) {
        showFlash(json.message, 'success');
        loadTrades();
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

// Filters
document.getElementById('statusFilter').addEventListener('change', loadTrades);
document.getElementById('symbolFilter').addEventListener('input', loadTrades);

// Load on page ready
loadTrades();
