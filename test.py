from src.pipelines.prediction_pipeline import PredictionPipeline

prediction_pipeline = PredictionPipeline()

predictions = prediction_pipeline.get_hybrid_recommendations(167885, 2204)

print(predictions)