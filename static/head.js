document.getElementById('predict-form').addEventListener('submit', async function(e) {
  e.preventDefault(); // prevent form refresh

  // Get values from inputs
  const hazard = parseFloat(document.getElementById('hazard').value);
  const exposure = parseFloat(document.getElementById('exposure').value);
  const housing = parseFloat(document.getElementById('housing').value);
  const poverty = parseFloat(document.getElementById('poverty').value);
  const vulnerability = parseFloat(document.getElementById('vulnerability').value);

  // Create data object
  const data = {
    Hazard_Intensity: hazard,
    Exposure: exposure,
    Housing: housing,
    Poverty: poverty,
    Vulnerability: vulnerability
  };

  try {
    // Send POST request to your FastAPI backend
    const response = await fetch('/predict', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    });

    const result = await response.json();

    // Show result in the page
    document.getElementById('result').innerText = `Predicted Severity: ${result.predicted_severity}`;
  } catch (error) {
    document.getElementById('result').innerText = 'Error: ' + error.message;
  }
});
