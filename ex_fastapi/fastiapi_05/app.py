from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import os

app=FastAPI(
    title="ML API Service"
)
model = None
MODEL_PATH = "models/iris.model.pkl"
IRIS_CLASSES = {}
IRIS_CLASSES = {}
IRIS_CLASSES = ["setosa", "versicolor", "virginica"]
class PredictionRequest(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float
class PredictionResponse(BaseModel):
    prediction_class: int
    prediction_name: str
@app.on_event("startup")
def load_model():
    global model
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
        print(f'model loaded from {MODEL_PATH}')
    else:
        print('Model not found')
@app.post("/predict",response_model=PredictionResponse)
def predict(request: PredictionRequest):
    global model
    if model is None:
        raise HTTPException(status_code=503, detail="Model is not loaded")
    features = [[
        request.sepal_length, request.sepal_width, request.petal_length, request.petal_width
    ]]
    prediction = model.predict(features)[0]
    prediction_name = IRIS_CLASSES[prediction]
    return PredictionResponse(
        prediction_class=int(prediction),prediction_name=prediction_name
    )
if __name__ == '__main__':
    import uvicorn
    uvicorn.run("app:app", host='127.0.0.1', port=8080, reload=True)
