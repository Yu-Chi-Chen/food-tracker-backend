class ImagePredictor:
    def __init__(self, prediction_instance):
        self.predictor = prediction_instance

    def predict(self, file_path):
        result = self.predictor.predict_image_classification_sample(
            filename=file_path)
        print("辨識結果: ", result[0]['displayNames'][0])
        return result[0]['displayNames'][0]
