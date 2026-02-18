// Gap Scanner
document.getElementById('scannerForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const minGap = document.getElementById('minGapInput').value;
    const direction = document.getElementById('directionSelect').value;
    const symbols = document.getElementById('symbolsInput').value.trim();
    const date = document.getElementById('dateInput').value;

    // Build query string
    let url = `/api/scanner/gaps?min_gap=${minGap}&direction=${direction}`;
    if (symbols) url += `&symbols=${encodeURIComponent(symbols)}`;
    if (date) url += `&date=${date}`;

    // Show loading
    document.getElementById('scannerLoading').classList.remove('d-none');
    document.getElementById('scannerResults').classList.add('d-none');
    document.getElementById('scannerNoResults').classList.add('d-none');

    try {
        const res = await fetch(url);
        const json = await res.json();
        const data = json.data;

        document.getElementById('scannerLoading').classList.add('d-none');

        if (data.total_found === 0) {
            document.getElementById('scannerNoResults').classList.remove('d-none');
            return;
        }

        document.getElementById('resultCount').textContent = data.total_found;
        document.getElementById('scanDate').textContent = data.scan_date;
        renderGaps(data.gaps);
        document.getElementById('scannerResults').classList.remove('d-none');
    } catch (err) {
        document.getElementById('scannerLoading').classList.add('d-none');
        showFlash('Scanner error: ' + err.message, 'danger');
    }
});

function renderGaps(gaps) {
    const tbody = document.getElementById('resultsBody');
    tbody.innerHTML = gaps.map(g => {
        const gapClass = g.direction === 'up' ? 'gap-up' : 'gap-down';
        const arrow = g.direction === 'up' ? '&#9650;' : '&#9660;';
        const volFormatted = (g.volume / 1e6).toFixed(1) + 'M';

        return `
        <tr data-testid="gap-row-${g.symbol}">
            <td><strong>${g.symbol}</strong></td>
            <td class="${gapClass}" data-testid="gap-percent-${g.symbol}">
                ${arrow} ${g.gap_percent > 0 ? '+' : ''}${g.gap_percent.toFixed(2)}%
            </td>
            <td class="${gapClass}">$${g.gap_amount > 0 ? '+' : ''}${g.gap_amount.toFixed(2)}</td>
            <td>$${g.prev_close.toFixed(2)}</td>
            <td>$${g.open.toFixed(2)}</td>
            <td>$${g.current.toFixed(2)}</td>
            <td>${volFormatted}</td>
            <td>${g.sector}</td>
            <td>
                <button class="btn btn-sm btn-outline-primary me-1" data-testid="add-watchlist-${g.symbol}"
                        onclick="addToWatchlist('${g.symbol}', '${g.sector}')">
                    Watch
                </button>
                <button class="btn btn-sm btn-outline-success" data-testid="open-trade-${g.symbol}"
                        onclick="openTrade('${g.symbol}', '${g.direction}', ${g.current}, ${g.gap_percent})">
                    Trade
                </button>
            </td>
        </tr>`;
    }).join('');
}

async function addToWatchlist(symbol, sector) {
    const res = await fetch('/api/watchlist/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ symbol, sector })
    });
    const json = await res.json();
    showFlash(json.message, res.ok ? 'success' : 'warning');
}

function openTrade(symbol, gapDirection, currentPrice, gapPercent) {
    // Redirect to journal with pre-filled params
    const params = new URLSearchParams({
        symbol, gap_type: 'gap_' + gapDirection,
        entry_price: currentPrice, gap_percent: gapPercent
    });
    window.location.href = `/journal?${params}`;
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
