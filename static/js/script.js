document.addEventListener("DOMContentLoaded", function () {
    console.log("JavaScript is working!");

    // Loan form handling
    const form = document.getElementById("loanForm");

    if (form) {
        form.addEventListener("submit", async (event) => {
            event.preventDefault(); // Prevent default form submission
            const formData = new FormData(form);
            const jsonData = Object.fromEntries(formData); // Convert form data to JSON

            try {
                const response = await fetch("/predict/", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify(jsonData), // Send JSON data to backend
                });

                const result = await response.json();
                if (result.eligibility) {
                    alert(`Eligibility: ${result.eligibility}`);
                } else {
                    alert(`Error: ${result.error || "Unexpected error occurred."}`);
                }
            } catch (error) {
                console.error("Error submitting loan form:", error);
                alert("Failed to submit loan form. Please try again.");
            }
        });
    }
});
