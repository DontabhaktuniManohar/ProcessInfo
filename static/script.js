const sitEnvironments = ["SIT1", "SIT2", "SIT3", "SIT4", "SIT5"];
const fixedEnvironments = ["PROD", "CANARY", "PRODE"];
const environmentSelect = document.getElementById("environment");
const flagSelect = document.getElementById("flag");
const form = document.getElementById("deploymentForm");
const responseDiv = document.getElementById("responseTable");

// Populate SIT Environment Dropdown
sitEnvironments.forEach(env => {
    const option = document.createElement("option");
    option.value = env;
    option.textContent = env;
    environmentSelect.appendChild(option);
});

// Handle Form Submission
form.addEventListener("submit", async function (e) {
    e.preventDefault();
    responseDiv.innerHTML = ""; // Clear previous results

    const selectedSIT = environmentSelect.value;
    const selectedFlag = flagSelect.value;

    if (!selectedSIT || !selectedFlag) {
        alert("Please select an environment and flag.");
        return;
    }

    // Include selected SIT + fixed environments
    const environmentsToCheck = [selectedSIT, ...fixedEnvironments];

    let sitCommitId = null; // To store SIT commit ID for comparison

    let tableHTML = `
        <table class="table table-bordered mt-4">
            <thead>
                <tr>
                    <th>Environment</th>
                    <th>Artifact</th>
                    <th>Commit</th>
                    <th>BG Flag</th>
                    <th>Deploy By</th>
                    <th>Status</th>
                    <th>Comparison</th>
                </tr>
            </thead>
            <tbody>
    `;

    for (let env of environmentsToCheck) {
        let bgflagValue = selectedFlag;

        if (fixedEnvironments.includes(env)) {
            bgflagValue = "NA"; // For fixed environments
        }

        const apiUrl = `http://localhost:5000/api/deployment?bgflag=${bgflagValue}&environment=${env}`;

        try {
            const response = await fetch(apiUrl);
            const result = await response.json();

            console.log(`Response for ${env}:`, result);

            if (result && result.status === "success" && Array.isArray(result.data) && result.data.length > 0) {
                const firstData = result.data[0]; // Get only the first record

                if (env === selectedSIT) {
                    sitCommitId = firstData.commit; // Store SIT commit ID
                }

                // Compare commit ID with SIT commit
                let comparisonStatus = "N/A";
                if (sitCommitId && env !== selectedSIT) {
                    comparisonStatus = firstData.commit === sitCommitId ? "SAME" : "DIFFERENT";
                }

                tableHTML += `
                    <tr>
                        <td>${firstData.environment}</td>
                        <td>${firstData.artifact}</td>
                        <td>${firstData.commit}</td>
                        <td>${firstData.bgflag}</td>
                        <td>${firstData.deployby}</td>
                        <td>${firstData.deploymentstatus}</td>
                        <td>${comparisonStatus}</td>
                    </tr>
                `;
            } else {
                tableHTML += `
                    <tr>
                        <td>${env}</td>
                        <td colspan="6" class="text-center text-muted">No Data Found</td>
                    </tr>
                `;
            }
        } catch (error) {
            console.error(`Error fetching API for ${env}:`, error);
            tableHTML += `
                <tr>
                    <td>${env}</td>
                    <td colspan="6" class="text-center text-danger">API Error</td>
                </tr>
            `;
        }
    }

    tableHTML += `</tbody></table>`;
    responseDiv.innerHTML = tableHTML;
});
