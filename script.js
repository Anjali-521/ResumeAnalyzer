document.getElementById("analyze").addEventListener("click", async () => {

    const fileInput = document.getElementById("resumeFile");
    const file = fileInput.files[0];

    if (!file) {
        alert("Please upload a resume first.");
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {

        const response = await fetch("/analyze", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        let output = "";

        output += "<h2>Detected Skills</h2>";
        output += "<ul>";

        data.skills.forEach(skill => {
            output += `<li>${skill}</li>`;
        });

        output += "</ul>";

        output += "<h2>Recommended Roles</h2>";
        output += "<ul>";

        data.recommended_roles.forEach(role => {
            output += `<li>${role}</li>`;
        });

        output += "</ul>";

        output += "<h2>Suggestions</h2>";
        output += "<ul>";

        data.mistakes.forEach(item => {
            output += `<li>${item}</li>`;
        });

        output += "</ul>";

        document.getElementById("result").innerHTML = output;

    } catch (error) {

        document.getElementById("result").innerHTML =
            "<p>Error analyzing resume.</p>";

        console.error(error);
    }

});