function initCharts(categoryLabels, categoryCounts, skillLabels, skillCounts) {
    const categoryCtx = document.getElementById('categoryChart');
    new Chart(categoryCtx, {
        type: 'pie',
        data: {
            labels: categoryLabels,
            datasets: [{
                data: categoryCounts,
                backgroundColor: ['#4e79a7', '#f28e2b', '#e15759', '#76b7b2']
            }]
        },
        options: {
            plugins: { title: { display: true, text: 'Predicted Category Distribution' } }
        }
    });

    const skillCtx = document.getElementById('skillChart');
    new Chart(skillCtx, {
        type: 'bar',
        data: {
            labels: skillLabels,
            datasets: [{
                label: 'Candidates with skill',
                data: skillCounts,
                backgroundColor: '#4e79a7'
            }]
        },
        options: {
            plugins: { title: { display: true, text: 'Skill Distribution' } }
        }
    });
}
document.addEventListener('DOMContentLoaded', function () {
    const filterInput = document.getElementById('filterInput');
    const table = document.getElementById('candidateTable');
    const rows = table.getElementsByTagName('tbody')[0].getElementsByTagName('tr');

    filterInput.addEventListener('keyup', function () {
        const searchTerm = filterInput.value.toLowerCase();

        for (let i = 0; i < rows.length; i++) {
            const categoryCell = rows[i].getElementsByTagName('td')[1];
            const categoryText = categoryCell.textContent.toLowerCase();

            if (categoryText.includes(searchTerm)) {
                rows[i].style.display = '';
            } else {
                rows[i].style.display = 'none';
            }
        }
    });
});