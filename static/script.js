document.getElementById('prediction-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent form from submitting the default way

    const formData = new FormData(this);
    const data = {};

    formData.forEach((value, key) => {
        data[key] = value;
    });

    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(result => {
        const predictions = result.predictions;

        if (predictions && predictions.length > 0) {
            document.getElementById('result').innerHTML = `
                <h2>Prediction Result</h2>
                <p>${predictions[0]}</p>
            `;
        } else {
            document.getElementById('result').innerHTML = `
                <h2>No Prediction Result</h2>
                <p>Unable to retrieve prediction result.</p>
            `;
        }
    })
    .catch(error => {
        document.getElementById('result').innerHTML = `
            <h2>Error</h2>
            <p>${error.message}</p>
        `;
    });
});
