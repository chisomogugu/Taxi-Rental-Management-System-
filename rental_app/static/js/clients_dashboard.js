document.addEventListener('DOMContentLoaded', function () {
    console.log(' JavaScript Loaded!');

    // State variables
    let models = [];
    const viewHistory = [];
    let selectedDate = '';
    let isBackNavigation = false;

    // UI elements
    const buttons = document.querySelectorAll('.book-btn');
    const inventoryModal = new bootstrap.Modal(document.getElementById('inventoryModal'));
    const inventoryList = document.getElementById('inventory-list');
    const backButton = document.getElementById('back-button');

    // Handle Book button clicks
    buttons.forEach(button => {
        button.addEventListener('click', function () {
            const brand = this.dataset.brand;
            console.log(` Book clicked for brand: ${brand}`);

            viewHistory.length = 0;
            viewHistory.push('models');
            isBackNavigation = false;
            backButton.style.display = 'none';

            fetch(`/client/book/${brand}`)
                .then(response => response.json())
                .then(data => {
                    models = data.models;
                    console.log(' Models fetched:', models);
                    displayModelTable();
                })
                .catch(err => {
                    console.error(' Fetch error:', err);
                    alert('Error loading car models. Try again.');
                });
        });
    });

    // Show model table
    function displayModelTable() {
        if (!isBackNavigation) viewHistory.push('models');
        isBackNavigation = false;

        let tableHTML = `
            <table class="table table-bordered">
                <thead>
                    <tr>
                        <th>Model ID</th>
                        <th>Year</th>
                        <th>Color</th>
                        <th>Transmission</th>
                    </tr>
                </thead>
                <tbody>
        `;

        models.forEach(model => {
            tableHTML += `
                <tr>
                    <td>${model.modelid}</td>
                    <td>${model.year}</td>
                    <td>${model.color}</td>
                    <td>${model.transmission}</td>
                </tr>
            `;
        });

        tableHTML += `
                </tbody>
            </table>
            <div class="text-center">
                <button id="next-btn" class="btn btn-primary mt-3">Next</button>
            </div>
        `;

        inventoryList.innerHTML = tableHTML;
        inventoryModal.show();

        // Wait until DOM is updated
        setTimeout(() => {
            document.getElementById('next-btn').addEventListener('click', showDateSelection);
        }, 0);
    }

    // Show date picker
    function showDateSelection() {
        if (!isBackNavigation) viewHistory.push('date');
        isBackNavigation = false;

        backButton.style.display = 'inline-block';

        let dateHTML = `
            <div class="text-center">
                <h5>Select a Rental Date</h5>
                <input type="date" id="rental-date" class="form-control w-50 mx-auto mt-3">
                <button id="check-availability" class="btn btn-success mt-3">Check Availability</button>
            </div>
        `;

        inventoryList.innerHTML = dateHTML;

        // Check availability on date click
        setTimeout(() => {
            document.getElementById('check-availability').addEventListener('click', function () {
                selectedDate = document.getElementById('rental-date').value;
                if (!selectedDate) {
                    alert('Please select a date.');
                    return;
                }
                showAvailability(selectedDate);
            });
        }, 0);
    }

    // Show available models for selected date
    async function showAvailability(date) {
        if (!isBackNavigation) viewHistory.push('availability');
        isBackNavigation = false;

        const results = await Promise.all(
            models.map(model =>
                fetch(`/client/check_availability/${model.modelid}?date=${date}`)
                    .then(res => res.json())
                    .then(data => ({
                        ...model,
                        available: data.available
                    }))
                    .catch(err => {
                        console.error(` Failed to check model ${model.modelid}:`, err);
                        return { ...model, available: false };
                    })
            )
        );

        let resultHTML = `
        <table class="table table-bordered">
            <thead>
                <tr>
                    <th>Model ID</th>
                    <th>Year</th>
                    <th>Color</th>
                    <th>Transmission</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
    `;

        results.forEach(model => {
            const buttonHTML = model.available
                ? `<button class="btn btn-success book-now-btn"
                            data-modelid="${model.modelid}"
                            data-date="${date}">Book Now</button>`
                : `<button class="btn btn-secondary" disabled>Not Available</button>`;

            resultHTML += `
                <tr>
                    <td>${model.modelid}</td>
                    <td>${model.year}</td>
                    <td>${model.color}</td>
                    <td>${model.transmission}</td>
                    <td>${buttonHTML}</td>
                </tr>
            `;
        });

        resultHTML += `</tbody></table>`;
        inventoryList.innerHTML = resultHTML;

        // Add Book Now button listeners
        setTimeout(() => attachBookNowHandlers(), 100);
    }

    // Handle confirm booking click
    function attachBookNowHandlers() {
        document.querySelectorAll('.book-now-btn').forEach(button => {
            button.addEventListener('click', function () {
                const modelid = this.dataset.modelid;
                const date = this.dataset.date;
                const model = models.find(m => m.modelid == modelid);

                const confirmHTML = `
                    <div class="text-center">
                        <h5>Confirm Your Booking</h5>
                        <p><strong>Car:</strong> ${model.name}</p>
                        <p><strong>Date:</strong> ${date}</p>
                        <button id="confirm-booking" class="btn btn-success mt-4">Confirm Booking</button>
                    </div>
                `;

                inventoryList.innerHTML = confirmHTML;

                if (!isBackNavigation) viewHistory.push('confirm');

                setTimeout(() => {
                    document.getElementById('confirm-booking').addEventListener('click', async () => {
                        try {
                            const res = await fetch('/client/confirm_booking', {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/json'
                                },
                                body: JSON.stringify({
                                    modelid: modelid,
                                    date: date
                                })
                            });

                            const result = await res.json();
                            if (result.success) {
                                alert(" Booking Confirmed!");
                                window.location.reload();
                            } else {
                                alert(" " + (result.error || "Booking failed."));
                            }
                        } catch (err) {
                            console.error(" Error submitting booking:", err);
                            alert("An error occurred while booking.");
                        }
                    });
                }, 0);
            });
        });
    }

    // Go back to previous step
    backButton.addEventListener('click', function () {
        if (viewHistory.length > 1) {
            viewHistory.pop();
            const previousView = viewHistory[viewHistory.length - 1];
            isBackNavigation = true;

            if (previousView === 'models') displayModelTable();
            else if (previousView === 'date') showDateSelection();
            else if (previousView === 'availability') showAvailability(selectedDate);

            isBackNavigation = false;
        }
    });
});
