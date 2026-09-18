document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('transaction-form');
    const transactionList = document.getElementById('transaction-list');
    const totalBalance = document.getElementById('total-balance');
    const totalIncome = document.getElementById('total-income');
    const totalExpenses = document.getElementById('total-expenses');
    
    // Set default date to today
    document.getElementById('date').valueToDate = new Date();
    document.getElementById('date').value = new Date().toISOString().split('T')[0];

    let myChart = null;

    // Fetch and display initial data
    fetchTransactions();

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const payload = {
            description: document.getElementById('description').value,
            amount: parseFloat(document.getElementById('amount').value),
            type: document.getElementById('type').value,
            category: document.getElementById('category').value,
            date: document.getElementById('date').value
        };

        const res = await fetch('/api/transactions', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (res.ok) {
            form.reset();
            document.getElementById('date').value = new Date().toISOString().split('T')[0];
            fetchTransactions();
        }
    });

    async function fetchTransactions() {
        const res = await fetch('/api/transactions');
        const transactions = await res.json();
        updateUI(transactions);
    }

    function updateUI(transactions) {
        transactionList.innerHTML = '';

        let incomeSum = 0;
        let expenseSum = 0;
        const categoryMap = {};

        transactions.forEach(tx => {
            const row = document.createElement('tr');
            const isIncome = tx.type === 'income';

            if (isIncome) incomeSum += tx.amount;
            else {
                expenseSum += tx.amount;
                categoryMap[tx.category] = (categoryMap[tx.category] || 0) + tx.amount;
            }

            row.innerHTML = `
                <td>${tx.date}</td>
                <td>${escapeHtml(tx.description)}</td>
                <td><small style="background:#eee; padding:2px 6px; border-radius:4px;">${escapeHtml(tx.category)}</small></td>
                <td class="${isIncome ? 'income-text' : 'expense-text'}">
                    ${isIncome ? '+' : '-'}$${tx.amount.toFixed(2)}
                </td>
                <td><button class="delete-btn" onclick="deleteTransaction(${tx.id})">✕</button></td>
            `;

            transactionList.appendChild(row);
        });

        // Update Totals
        totalIncome.textContent = `$${incomeSum.toFixed(2)}`;
        totalExpenses.textContent = `$${expenseSum.toFixed(2)}`;
        const balance = incomeSum - expenseSum;
        totalBalance.textContent = `$${balance.toFixed(2)}`;

        renderChart(categoryMap);
    }

    window.deleteTransaction = async function(id) {
        if (confirm('Delete this transaction?')) {
            await fetch(`/api/transactions/${id}`, { method: 'DELETE' });
            fetchTransactions();
        }
    };

    function renderChart(categoryMap) {
        const ctx = document.getElementById('expenseChart').getContext('2d');
        const labels = Object.keys(categoryMap);
        const data = Object.values(categoryMap);

        if (myChart) {
            myChart.destroy();
        }

        myChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels.length ? labels : ['No Expenses'],
                datasets: [{
                    data: data.length ? data : [1],
                    backgroundColor: [
                        '#e74c3c', '#3498db', '#f1c40f', '#9b59b6',
                        '#e67e22', '#1abc9c', '#34495e'
                    ]
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    title: { display: true, text: 'Expenses by Category' }
                }
            }
        });
    }

    function escapeHtml(str) {
        return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
    }
});


