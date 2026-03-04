document.getElementById("fetchBtn").addEventListener("click", async () => {
    const userId = document.getElementById("userId").value;
    const resultDiv = document.getElementById("result");

    if (!userId) {
        alert("Please enter a user ID");
        return;
    }

    // Loading indicator
    resultDiv.innerHTML = "Loading...";

    try {
        // Update URL to include the correct port (8001)
        const response = await fetch(`http://127.0.0.1:8001/user/redis/${userId}`);
        console.log("Response status:", response.status);

        // Check if response is OK
        if (!response.ok) {
            resultDiv.innerHTML = "❌ Failed to fetch data (Server error)";
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        // Parse JSON
        const data = await response.json();
        console.log("Fetched data:", data);

        // Show result and source message
        const sourceMessage = data.source === "cache" ? "Fetched from cache" : "Fetched from DB";

        // Show the fetched user and source of the data
        resultDiv.innerHTML = `
            <p><strong>ID:</strong> ${data.data.id}</p>
            <p><strong>Name:</strong> ${data.data.name}</p>
            <p><em>${sourceMessage}</em></p>
        `;
    } catch (err) {
        // Error handling
        resultDiv.innerHTML = "❌ Error fetching data";
        console.error("Fetch error:", err);
    }
});