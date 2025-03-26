document.addEventListener('DOMContentLoaded', function () {
    const sitEnvironments = ["SIT1", "SIT2", "SIT3", "SIT4", "SIT5"];
    const fixedEnvironments = ["PROD", "CANARY", "PRODE"];  // Always included
    const environmentSelect = document.getElementById('environment');
    const flagSelect = document.getElementById('flag');
    const form = document.getElementById('deploymentForm');
    const responseDiv = document.getElementById('responseTable');

    // Populate SIT Environment Dropdown
    sitEnvironments.forEach(env => {
        const option = document.createElement('option');
        option.value = env;
        option.textContent = env;
        environmentSelect.appendChild(option);
    });

    // Handle Form Submission
    form.addEventListener('submit', async function (e) {
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
                    </tr>
                </thead>
                <tbody>
        `;

        // Loop through environments and fetch data
        for (let env of environmentsToCheck) {
            let bgflagValue = selectedFlag; // Default for SIT environments

            // If it's a fixed environment, set bgflag to NA
            if (fixedEnvironments.includes(env)) {
                bgflagValue = "NA";
            }

            const apiUrl = `http://localhost:5000/api/deployment?bgflag=${bgflagValue}&environment=${env}`;
            
            try {
                const response = await fetch(apiUrl);
                const data = await response.json();
                
                if (Object.keys(data).length > 0) {  // Check if API returned data
                    tableHTML += `
                        <tr>
                            <td>${data.environment}</td>
                            <td>${data.artifact}</td>
                            <td>${data.commit}</td>
                            <td>${data.bgflag}</td>
                            <td>${data.deployby}</td>
                            <td>${data.deploymentstatus}</td>
                        </tr>
                    `;
                } else {
                    tableHTML += `
                        <tr>
                            <td>${env}</td>
                            <td colspan="5" class="text-center text-muted">No Data Found</td>
                        </tr>
                    `;
                }
            } catch (error) {
                console.error("Error fetching API:", error);
                tableHTML += `
                    <tr>
                        <td>${env}</td>
                        <td colspan="5" class="text-center text-danger">API Error</td>
                    </tr>
                `;
            }
        }

        tableHTML += `</tbody></table>`;
        responseDiv.innerHTML = tableHTML;
    });
});
