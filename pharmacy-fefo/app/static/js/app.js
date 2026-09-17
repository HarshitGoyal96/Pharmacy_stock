// ================================
// AUTH TABS
// ================================

function showLogin() {
    document.getElementById("login-form").style.display = "flex";
    document.getElementById("register-form").style.display = "none";

    document.getElementById("login-tab").classList.add("active");
    document.getElementById("register-tab").classList.remove("active");

    document.getElementById("auth-message").textContent = "";
}


function showRegister() {
    document.getElementById("login-form").style.display = "none";
    document.getElementById("register-form").style.display = "flex";

    document.getElementById("login-tab").classList.remove("active");
    document.getElementById("register-tab").classList.add("active");

    document.getElementById("auth-message").textContent = "";
}


// ================================
// REGISTER
// ================================

document
    .getElementById("register-form")
    .addEventListener("submit", async function(event) {

        event.preventDefault();

        const name = document.getElementById("register-name").value;
        const email = document.getElementById("register-email").value;
        const password = document.getElementById("register-password").value;

        const message = document.getElementById("auth-message");

        try {

            const response = await fetch("/api/auth/register", {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    name: name,
                    email: email,
                    password: password
                })
            });

            const data = await response.json();

            if (!response.ok) {
                message.textContent = data.detail || "Registration failed";
                message.style.color = "red";
                return;
            }

            message.textContent = "Registration successful! Please login.";
            message.style.color = "green";

            document.getElementById("register-form").reset();

            setTimeout(() => {
                showLogin();
            }, 1000);

        } catch (error) {

            console.error(error);

            message.textContent = "Unable to connect to server.";
            message.style.color = "red";
        }
    });


// ================================
// LOGIN
// ================================

document
    .getElementById("login-form")
    .addEventListener("submit", async function(event) {

        event.preventDefault();

        const email = document.getElementById("login-email").value;
        const password = document.getElementById("login-password").value;

        const message = document.getElementById("auth-message");

        try {

            const response = await fetch("/api/auth/login", {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    email: email,
                    password: password
                })
            });

            const data = await response.json();

            if (!response.ok) {
                message.textContent = data.detail || "Login failed";
                message.style.color = "red";
                return;
            }

            // Save authentication information
            localStorage.setItem(
                "access_token",
                data.access_token
            );

            localStorage.setItem(
                "user",
                JSON.stringify(data.user)
            );

            showDashboard(data.user);

        } catch (error) {

            console.error(error);

            message.textContent = "Unable to connect to server.";
            message.style.color = "red";
        }
    });


// ================================
// SHOW DASHBOARD
// ================================

function showDashboard(user) {

    document.getElementById("auth-section").style.display = "none";

    document.getElementById("dashboard").style.display = "block";

    document.getElementById("welcome-user").textContent =
        `Welcome, ${user.name}`;

    loadMedicines();
    loadAlerts();
}


// ================================
// LOGOUT
// ================================

function logout() {

    localStorage.removeItem("access_token");
    localStorage.removeItem("user");

    document.getElementById("dashboard").style.display = "none";

    document.getElementById("auth-section").style.display = "flex";

    showLogin();
}


// ================================
// MEDICINES
// ================================

let currentPage = 1;
const pageSize = 10;
let totalPages = 1;


async function loadMedicines() {

    const search =
        document.getElementById("search-input").value;

    const sortBy =
        document.getElementById("sort-by").value;

    const sortOrder =
        document.getElementById("sort-order").value;

    const url =
        `/api/medicines/?search=${encodeURIComponent(search)}` +
        `&page=${currentPage}` +
        `&page_size=${pageSize}` +
        `&sort_by=${sortBy}` +
        `&order=${sortOrder}`;

    try {

        const response = await fetch(url);

        const data = await response.json();

        if (!response.ok) {
            console.error(data);
            return;
        }

        totalPages = data.total_pages || 1;

        const table =
            document.getElementById("medicine-table");

        table.innerHTML = "";

        if (data.medicines.length === 0) {

            table.innerHTML = `
                <tr>
                    <td colspan="6" style="text-align:center;">
                        No medicines found
                    </td>
                </tr>
            `;

        } else {

            data.medicines.forEach(medicine => {

                const row = document.createElement("tr");

                row.innerHTML = `
                    <td>${medicine.id}</td>

                    <td>
                        <strong>${medicine.name}</strong>
                    </td>

                    <td>
                        ${medicine.generic_name || "-"}
                    </td>

                    <td>
                        ${medicine.manufacturer || "-"}
                    </td>

                    <td class="stock">
                        ${medicine.sellable_stock}
                    </td>

                    <td>

    <button
        class="action-btn"
        onclick="viewBatches(
            ${medicine.id}
        )"
    >
        View Batches
    </button>

    <button
        class="action-btn"
        onclick="openBatchForm(
            ${medicine.id},
            '${medicine.name.replace(/'/g, "\\'")}'
        )"
    >
        Add Batch
    </button>

    <button
        class="action-btn"
        onclick="openDispenseForm(
            ${medicine.id},
            '${medicine.name.replace(/'/g, "\\'")}'
        )"
    >
        Dispense
    </button>

</td>
                `;

                table.appendChild(row);
            });
        }

        document.getElementById("page-info").textContent =
            `Page ${data.page} of ${totalPages}`;

    } catch (error) {

        console.error("Error loading medicines:", error);
    }
}


// ================================
// PAGINATION
// ================================

function nextPage() {

    if (currentPage < totalPages) {
        currentPage++;
        loadMedicines();
    }
}


function previousPage() {

    if (currentPage > 1) {
        currentPage--;
        loadMedicines();
    }
}


// ================================
// EXPIRY ALERTS
// ================================

async function loadAlerts() {

    const container =
        document.getElementById("alerts-container");

    try {

        const response =
            await fetch("/api/medicines/alerts/expiring?days=30");

        const data = await response.json();

        if (!response.ok) {
            container.textContent = "Unable to load alerts.";
            return;
        }

        if (data.alerts.length === 0) {

            container.innerHTML = `
                <div class="no-alerts">
                    ✓ No batches are expiring within 30 days.
                </div>
            `;

            return;
        }

        container.innerHTML = "";

        data.alerts.forEach(alert => {

            const item = document.createElement("div");

            item.className = "alert-item";

            item.innerHTML = `
                <strong>${alert.medicine}</strong>

                <br>

                Batch:
                ${alert.batch_number}

                <br>

                Quantity:
                ${alert.quantity}

                <br>

                Expiry:
                ${alert.expiry_date}

                <br>

                <strong>
                    ${alert.days_until_expiry} days remaining
                </strong>
            `;

            container.appendChild(item);
        });

    } catch (error) {

        console.error("Error loading alerts:", error);

        container.textContent =
            "Unable to connect to server.";
    }
}


// ================================
// MEDICINE MODAL
// ================================

function openMedicineForm() {

    document.getElementById("medicine-modal").style.display = "flex";
}


function closeMedicineForm() {

    document.getElementById("medicine-modal").style.display = "none";
}


// ================================
// ADD MEDICINE
// ================================

document
    .getElementById("medicine-form")
    .addEventListener("submit", async function(event) {

        event.preventDefault();

        const name =
            document.getElementById("medicine-name").value;

        const genericName =
            document.getElementById("generic-name").value;

        const manufacturer =
            document.getElementById("manufacturer").value;

        const message =
            document.getElementById("medicine-message");

        try {

            const response = await fetch("/api/medicines/", {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    name: name,
                    generic_name: genericName || null,
                    manufacturer: manufacturer || null
                })
            });

            const data = await response.json();

            if (!response.ok) {

                message.textContent =
                    data.detail || "Unable to add medicine";

                message.style.color = "red";

                return;
            }

            message.textContent =
                "Medicine added successfully!";

            message.style.color = "green";

            document
                .getElementById("medicine-form")
                .reset();

            loadMedicines();

            setTimeout(() => {
                closeMedicineForm();
                message.textContent = "";
            }, 1000);

        } catch (error) {

            console.error(error);

            message.textContent =
                "Unable to connect to server.";

            message.style.color = "red";
        }
    });


// ================================
// VIEW BATCHES
// ================================

async function viewBatches(medicineId) {

    try {

        const response =
            await fetch(
                `/api/medicines/${medicineId}/batches`
            );

        const data = await response.json();

        if (!response.ok) {
            alert(data.detail || "Unable to load batches");
            return;
        }

        let message =
            `${data.medicine} Batches\n\n`;

        if (data.batches.length === 0) {

            message += "No batches found.";

        } else {

            data.batches.forEach(batch => {

                message +=
                    `Batch: ${batch.batch_number}\n` +
                    `Quantity: ${batch.quantity}\n` +
                    `Expiry: ${batch.expiry_date}\n` +
                    `Status: ${
                        batch.expired
                            ? "EXPIRED"
                            : "SELLABLE"
                    }\n\n`;
            });
        }

        alert(message);

    } catch (error) {

        console.error(error);

        alert("Unable to connect to server.");
    }
}


// ================================
// AUTO LOGIN
// ================================

window.addEventListener("DOMContentLoaded", () => {

    const token =
        localStorage.getItem("access_token");

    const userString =
        localStorage.getItem("user");

    if (token && userString) {

        try {

            const user = JSON.parse(userString);

            showDashboard(user);

        } catch (error) {

            logout();
        }
    }

});

// ================================
// ADD BATCH
// ================================

let selectedMedicineId = null;


function openBatchForm(medicineId, medicineName) {

    selectedMedicineId = medicineId;

    document.getElementById(
        "batch-medicine-name"
    ).textContent = `Medicine: ${medicineName}`;

    document.getElementById(
        "batch-modal"
    ).style.display = "flex";
}


function closeBatchForm() {

    document.getElementById(
        "batch-modal"
    ).style.display = "none";

    document.getElementById(
        "batch-form"
    ).reset();

    document.getElementById(
        "batch-message"
    ).textContent = "";
}


document
    .getElementById("batch-form")
    .addEventListener("submit", async function(event) {

        event.preventDefault();

        const batchNumber =
            document.getElementById("batch-number").value;

        const quantity =
            parseInt(
                document.getElementById("batch-quantity").value
            );

        const expiryDate =
            document.getElementById("batch-expiry").value;

        const message =
            document.getElementById("batch-message");

        try {

            const response = await fetch(
                `/api/medicines/${selectedMedicineId}/batches`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        batch_number: batchNumber,
                        quantity: quantity,
                        expiry_date: expiryDate
                    })
                }
            );

            const data = await response.json();

            if (!response.ok) {

                message.textContent =
                    data.detail || "Unable to add batch";

                message.style.color = "red";

                return;
            }

            message.textContent =
                "Batch added successfully!";

            message.style.color = "green";

            loadMedicines();

            setTimeout(() => {
                closeBatchForm();
            }, 800);

        } catch (error) {

            console.error(error);

            message.textContent =
                "Unable to connect to server.";

            message.style.color = "red";
        }
    });
// ================================
// DISPENSE MEDICINE
// ================================

let dispenseMedicineId = null;


function openDispenseForm(medicineId, medicineName) {

    dispenseMedicineId = medicineId;

    document.getElementById(
        "dispense-medicine-name"
    ).textContent = `Medicine: ${medicineName}`;

    document.getElementById(
        "dispense-modal"
    ).style.display = "flex";
}


function closeDispenseForm() {

    document.getElementById(
        "dispense-modal"
    ).style.display = "none";

    document.getElementById(
        "dispense-form"
    ).reset();

    document.getElementById(
        "dispense-result"
    ).innerHTML = "";
}


document
    .getElementById("dispense-form")
    .addEventListener("submit", async function(event) {

        event.preventDefault();

        const quantity =
            parseInt(
                document.getElementById(
                    "dispense-quantity"
                ).value
            );

        const result =
            document.getElementById(
                "dispense-result"
            );

        try {

            const response = await fetch(
                `/api/medicines/${dispenseMedicineId}/dispense`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        quantity: quantity
                    })
                }
            );

            const data = await response.json();

            if (!response.ok) {

                result.innerHTML = `
                    <p style="color:red;">
                        ${
                            data.detail?.message ||
                            data.detail ||
                            "Dispensing failed"
                        }
                    </p>
                `;

                return;
            }

            let html = `
                <div class="success-result">

                    <p>
                        <strong>
                            ✓ ${data.quantity_dispensed}
                            units dispensed
                        </strong>
                    </p>

                    <p>
                        FEFO batches used:
                    </p>
            `;

            data.dispensed_from.forEach(batch => {

                html += `
                    <div class="alert-item">

                        Batch:
                        <strong>
                            ${batch.batch_number}
                        </strong>

                        <br>

                        Expiry:
                        ${batch.expiry_date}

                        <br>

                        Quantity dispensed:
                        ${batch.quantity_dispensed}

                        <br>

                        Remaining:
                        ${batch.remaining_in_batch}

                    </div>
                `;
            });

            html += `</div>`;

            result.innerHTML = html;

            loadMedicines();
            loadAlerts();

        } catch (error) {

            console.error(error);

            result.innerHTML = `
                <p style="color:red;">
                    Unable to connect to server.
                </p>
            `;
        }
    });