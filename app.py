from fastapi import FastAPI
from pydantic import BaseModel
import joblib

# Load model
model = joblib.load("earthquake_severity_model.joblib")

# Define label map
label_map = {
    0: 'Highest',
    1: 'High',
    2: 'Low',
    3: 'Moderate',
    4: 'Medium',
    5: 'Lower',
    6: 'Very Low'
}

app = FastAPI()

class InputData(BaseModel):
    Hazard_Intensity: float
    Exposure: float
    Housing: float
    Poverty: float
    Vulnerability: float

@app.post("/predict")
def predict(data: InputData):
    input_data = [
        data.Hazard_Intensity,
        data.Exposure,
        data.Housing,
        data.Poverty,
        data.Vulnerability
    ]
    prediction = model.predict([input_data])
    predicted_class = int(prediction[0])
    predicted_label = label_map.get(predicted_class, "Unknown")
    return {"predicted_severity": predicted_label}
@app.get("/")
def home():
    return {"message": "Welcome to Earthquake Severity Prediction API"}

