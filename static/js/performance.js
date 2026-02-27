// Performance Dashboard
let cumulativeChart = null;
let dailyChart = null;
let gapTypeChart = null;

async function loadStats() {
    const days = document.getElementById('periodFilter').value;

    // Fetch all stats in parallel
    const [summaryRes, seriesRes, gapTypeRes] = await Promise.all([
        fetch(`${BASE_PATH}/api/stats/summary`),
        fetch(`${BASE_PATH}/api/stats/pnl-series?days=${days}`),
        fetch(`${BASE_PATH}/api/stats/by-gap-type`)
    ]);

    const summary = (await summaryRes.json()).data;
    const series = (await seriesRes.json()).data;
    const gapTypes = (await gapTypeRes.json()).data;

    renderSummaryCards(summary);
    renderCumulativeChart(series);
    renderDailyChart(series);
    renderGapTypeChart(gapTypes);
}

function renderSummaryCards(s) {
    document.getElementById('statsTotalTrades').textContent = s.total_trades;
    document.getElementById('statsWinRate').textContent = s.win_rate + '%';
    document.getElementById('statsWinRate').className = s.win_rate >= 50 ? 'pnl-positive' : 'pnl-negative';

    const pnlEl = document.getElementById('statsTotalPnl');
    pnlEl.textContent = '$' + s.total_pnl.toFixed(2);
    pnlEl.className = s.total_pnl >= 0 ? 'pnl-positive' : 'pnl-negative';

    document.getElementById('statsProfitFactor').textContent = s.profit_factor.toFixed(2);

    const bestEl = document.getElementById('statsBestTrade');
    bestEl.textContent = '$' + s.best_trade.toFixed(2);
    bestEl.className = 'pnl-positive';

    const worstEl = document.getElementById('statsWorstTrade');
    worstEl.textContent = '$' + s.worst_trade.toFixed(2);
    worstEl.className = 'pnl-negative';

    document.getElementById('statsAvgWinner').textContent = '$' + s.avg_winner.toFixed(2);
    document.getElementById('statsAvgLoser').textContent = '$' + s.avg_loser.toFixed(2);
}

function renderCumulativeChart(series) {
    const ctx = document.getElementById('cumulativePnlChart').getContext('2d');
    if (cumulativeChart) cumulativeChart.destroy();

    cumulativeChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: series.labels,
            datasets: [{
                label: 'Cumulative P&L',
                data: series.cumulative_pnl,
                borderColor: '#0d6efd',
                backgroundColor: 'rgba(13, 110, 253, 0.1)',
                fill: true,
                tension: 0.3
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: { ticks: { callback: v => '$' + v } }
            }
        }
    });
}

function renderDailyChart(series) {
    const ctx = document.getElementById('dailyPnlChart').getContext('2d');
    if (dailyChart) dailyChart.destroy();

    const colors = series.daily_pnl.map(v => v >= 0 ? '#198754' : '#dc3545');

    dailyChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: series.labels,
            datasets: [{
                label: 'Daily P&L',
                data: series.daily_pnl,
                backgroundColor: colors
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: { ticks: { callback: v => '$' + v } }
            }
        }
    });
}

function renderGapTypeChart(gapTypes) {
    const ctx = document.getElementById('gapTypeChart').getContext('2d');
    if (gapTypeChart) gapTypeChart.destroy();

    gapTypeChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Gap Up', 'Gap Down'],
            datasets: [{
                data: [
                    gapTypes.gap_up ? gapTypes.gap_up.count : 0,
                    gapTypes.gap_down ? gapTypes.gap_down.count : 0
                ],
                backgroundColor: ['#198754', '#dc3545']
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { position: 'bottom' }
            }
        }
    });
}

// Period filter
document.getElementById('periodFilter').addEventListener('change', loadStats);

// Load on page ready
loadStats();
