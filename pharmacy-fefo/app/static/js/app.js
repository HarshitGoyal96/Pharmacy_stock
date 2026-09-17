async function checkAPI() {
    const status = document.getElementById("api-status");

    try {
        const response = await fetch("/api/health");
        const data = await response.json();

        status.textContent = data.message;
    } catch (error) {
        status.textContent = "API connection failed";
        console.error(error);
    }
}