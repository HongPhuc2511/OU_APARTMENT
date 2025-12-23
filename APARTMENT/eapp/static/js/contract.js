
document.addEventListener('DOMContentLoaded', function() {
    const startDateInput = document.getElementById('start_date');
    const durationSelect = document.getElementById('duration');
    const endDateInput = document.getElementById('end_date');

    function calculateEndDate() {
        const startDateValue = startDateInput.value;
        const durationValue = durationSelect.value;

        if (!startDateValue || !durationValue) return;

        let startDate;
        if (startDateValue.includes('/')) {
            const parts = startDateValue.split('/');
            startDate = new Date(parts[2], parts[1] - 1, parts[0]);
        } else {
            startDate = new Date(startDateValue);
        }

        let endDate = new Date(startDate);

        if (durationValue === 'SIX_MONTHS') {
            endDate.setMonth(endDate.getMonth() + 6);
        } else if (durationValue === 'ONE_YEAR') {
            endDate.setFullYear(endDate.getFullYear() + 1);
        }

        const day = String(endDate.getDate()).padStart(2, '0');
        const month = String(endDate.getMonth() + 1).padStart(2, '0');
        const year = endDate.getFullYear();

        // Format YYYY-MM-DD cho cả hiển thị và server
        const formattedDate = `${year}-${month}-${day}`;

        endDateInput.removeAttribute('readonly');
        endDateInput.value = formattedDate;
        endDateInput.setAttribute('readonly', 'readonly');
    }

    let lastStartDate = '';
    let lastDuration = '';

    setInterval(function() {
        if (startDateInput.value !== lastStartDate ||
            durationSelect.value !== lastDuration) {
            lastStartDate = startDateInput.value;
            lastDuration = durationSelect.value;
            calculateEndDate();
        }
    }, 300);

    durationSelect.addEventListener('change', calculateEndDate);
});