from fastapi import FastAPI
import uvicorn

from src import logger
from src.pipelines.prediction_pipeline import PredictionPipeline

prediction_pipeline = PredictionPipeline()

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "App is running!"}

@app.get("/prediction")
async def get_prediction(user_id, item_id):
    prediction_df = prediction_pipeline.get_hybrid_recommendations(
        user_id=int(user_id),
        parent_asin=int(item_id))
    return prediction_df.to_dict(orient="records")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)