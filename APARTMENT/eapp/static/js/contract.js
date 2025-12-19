document.addEventListener("DOMContentLoaded", function () {
    const startDate = document.getElementById("start_date");
    const duration = document.getElementById("duration");
    const endDate = document.getElementById("end_date");

    function calculateEndDate() {
        if (!startDate?.value || !duration?.value) return;

        let start = new Date(startDate.value);

        if (duration.value === "SIX_MONTHS") {
            start.setMonth(start.getMonth() + 6);
        } else if (duration.value === "ONE_YEAR") {
            start.setFullYear(start.getFullYear() + 1);
        }

        const yyyy = start.getFullYear();
        const mm = String(start.getMonth() + 1).padStart(2, '0');
        const dd = String(start.getDate()).padStart(2, '0');

        endDate.value = `${yyyy}-${mm}-${dd}`;
    }

    startDate?.addEventListener("change", calculateEndDate);
    duration?.addEventListener("change", calculateEndDate);
});