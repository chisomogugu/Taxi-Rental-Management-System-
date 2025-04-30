document.addEventListener('DOMContentLoaded', function () {
    fetchRentalData(); // Load rental history

    const modal = document.getElementById('reviewModal');
    const closeModal = document.querySelector('#reviewModal .close');
    const nextBtn = document.getElementById('submitReviewBtn');
    let currentDriver = null;

    // Close modal when (x) is clicked
    closeModal.onclick = () => {
        modal.style.display = 'none';
        resetModal();
    };

    // Close modal when clicked outside
    window.onclick = function (event) {
        if (event.target == modal) {
            modal.style.display = 'none';
            resetModal();
        }
    };

    // Fetch rental history data
    function fetchRentalData() {
        fetch('/client/my_rentals')
            .then(response => response.json())
            .then(data => {
                const tbody = document.getElementById('rental-history-body');
                tbody.innerHTML = '';
                data.forEach(rent => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${rent.rentid}</td>
                        <td>${rent.date}</td>
                        <td>${rent.drivername}</td>
                        <td>${rent.constructionyear}</td>
                        <td>${rent.color}</td>
                        <td>${rent.transmissiontype}</td>
                        <td>
                            ${rent.canReview ? 
                                `<button class="btn btn-pink btn-sm review-btn" data-driver="${rent.drivername}">Review</button>` :
                                `<button class="btn btn-secondary btn-sm" disabled>Reviewed</button>`
                            }
                        </td>
                    `;
                    tbody.appendChild(row);
                });

                // Add click handler to Review buttons
                document.querySelectorAll('.review-btn').forEach(btn => {
                    btn.addEventListener('click', (e) => {
                        currentDriver = btn.getAttribute('data-driver');
                        modal.style.display = 'block';
                    });
                });
            })
            .catch(() => alert("Could not fetch rental data."));
    }

    // Submit review
    nextBtn.onclick = () => {
        const message = document.getElementById('reviewMessage').value.trim();
        const rating = document.getElementById('reviewRating').value;

        if (!message || !rating) {
            alert('Please provide both review and rating.');
            return;
        }

        fetch('/client/submit_review', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                drivername: currentDriver,
                message: message,
                rating: rating
            })
        })
        .then(response => response.json())
        .then(result => {
            if (result.message) {
                alert(result.message);
                modal.style.display = 'none';
                resetModal();
                fetchRentalData(); // Refresh table
            } else {
                alert("Failed to submit review.");
            }
        })
        .catch(() => alert("Failed to submit review."));
    };

    // Reset modal inputs
    function resetModal() {
        document.getElementById('reviewMessage').value = '';
        document.getElementById('reviewRating').value = '';
    }
});
