document.addEventListener('DOMContentLoaded', function () {

    const selector = document.getElementById('reportSelector');

    if (!selector) return;

    selector.addEventListener('change', function () {
        const sections = document.querySelectorAll('.report-section');
        const selectedValue = this.value;

        sections.forEach(section => {
            if (selectedValue === 'all') {
                section.classList.remove('d-none');
            } else {
                section.classList.add('d-none');
            }
        });

        if (selectedValue !== 'all') {
            const targetSection = document.getElementById(selectedValue);
            if (targetSection) {
                targetSection.classList.remove('d-none');
            }
        }
    });


});

