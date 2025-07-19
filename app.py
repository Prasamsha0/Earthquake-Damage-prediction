from fastapi import FastAPI, Request, Form
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import joblib

# Load the model
model = joblib.load("earthquake_severity_model.joblib")

# Label map
label_map = {
    0: 'Highest',
    1: 'High',
    2: 'Low',
    3: 'Moderate',
    4: 'Medium',
    5: 'Lower',
    6: 'Very Low'
}

# FastAPI app
app = FastAPI()

# Mount static folder
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve HTML file directly
@app.get("/")
def read_index():
    return FileResponse("static/home.html")

# Define input model for JSON
class PredictionInput(BaseModel):
    Hazard_Intensity: float
    Exposure: float
    Housing: float
    Poverty: float
    Vulnerability: float

# Handle form POST (now expects JSON)
@app.post("/predict")
async def predict(data: PredictionInput):
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
