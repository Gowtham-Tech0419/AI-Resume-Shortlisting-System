function showSection(sectionId) {
    document.querySelectorAll('.tab-section').forEach(function (section) {
        section.classList.remove('active');
    });
    document.getElementById(sectionId).classList.add('active');

    document.querySelectorAll('.tab-btn').forEach(function (btn) {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');
}
document.getElementById('resumeForm').addEventListener('submit', function (event) {
    event.preventDefault();

    const formData = new FormData(this);
    const resultBox = document.getElementById('resumeResult');

    fetch('/api/upload_resume', { method: 'POST', body: formData })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                resultBox.className = 'result-box success';
                resultBox.innerHTML =
                    'Resume uploaded! Predicted category: <strong>' + data.predicted_category + '</strong><br>' +
                    'Detected skills: ' + data.detected_skills.join(', ');
            } else {
                resultBox.className = 'result-box error';
                resultBox.innerHTML = data.message;
            }
        })
        .catch(function () {
            resultBox.className = 'result-box error';
            resultBox.innerHTML = 'Something went wrong. Please try again.';
        });
});

document.getElementById('jdForm').addEventListener('submit', function (event) {
    event.preventDefault();

    const formData = new FormData(this);
    const resultBox = document.getElementById('jdResult');

    fetch('/api/submit_jd', { method: 'POST', body: formData })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                resultBox.className = 'result-box success';
                resultBox.innerHTML =
                    'Job saved! ID: <strong>' + data.job_id + '</strong><br>' +
                    'Required skills detected: ' + data.required_skills.join(', ');
                document.getElementById('jobSelect').innerHTML +=
                    '<option value="' + data.job_id + '">' + data.title + ' (ID ' + data.job_id + ')</option>';
            } else {
                resultBox.className = 'result-box error';
                resultBox.innerHTML = data.message;
            }
        })
        .catch(function () {
            resultBox.className = 'result-box error';
            resultBox.innerHTML = 'Something went wrong. Please try again.';
        });
});

function goToDashboard() {
    const jobId = document.getElementById('jobSelect').value;
    if (!jobId) {
        alert('Please select a job first.');
        return;
    }
    window.location.href = '/dashboard/' + jobId;
}