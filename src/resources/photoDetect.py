import base64

from google.cloud import aiplatform
from google.cloud.aiplatform.gapic.schema import predict


class ImageClassificationPredictionInstance:
    def __init__(self, project, endpoint_id, location, api_endpoint):
        self.project = project
        self.endpoint_id = endpoint_id
        self.location = location
        self.api_endpoint = api_endpoint
        self.client_options = {"api_endpoint": api_endpoint}
        self.client = aiplatform.gapic.PredictionServiceClient(
            client_options=self.client_options)
        self.endpoint = self.client.endpoint_path(
            project=project, location=location, endpoint=endpoint_id)

    def predict_image_classification_sample(
        self,
        filename: str,
    ):
        with open(filename, "rb") as f:
            file_content = f.read()

        # The format of each instance should conform to the deployed model's prediction input schema.
        encoded_content = base64.b64encode(file_content).decode("utf-8")
        instance = predict.instance.ImageClassificationPredictionInstance(
            content=encoded_content,
        ).to_value()
        instances = [instance]
        # See gs://google-cloud-aiplatform/schema/predict/params/image_classification_1.0.0.yaml for the format of the parameters.
        parameters = predict.params.ImageClassificationPredictionParams(
            confidence_threshold=0.5,
            max_predictions=5,
        ).to_value()

        response = self.client.predict(
            endpoint=self.endpoint, instances=instances, parameters=parameters
        )
        print("response")
        print(" deployed_model_id:", response.deployed_model_id)
        # See gs://google-cloud-aiplatform/schema/predict/prediction/image_classification_1.0.0.yaml for the format of the predictions.
        predictions = response.predictions
        for prediction in predictions:
            print(" prediction:", dict(prediction))

        return predictions


# # 使用示例
# if __name__ == "__main__":
#     # 替换以下信息为你的实际信息
#     project_id = "559469432498"
#     endpoint_id = "6637446032651190272"

#     # create instance
#     prediction_instance = ImageClassificationPredictionInstance(
#         project=project_id,
#         endpoint_id=endpoint_id
#     )

#     # 替换以下信息为你的实际图片文件路径
#     image_files = [
#         "path_to_your_image1.jpg",
#         "path_to_your_image2.jpg",
#         # ... 可以继续添加更多图片文件路径
#     ]

#     # 对每个图片文件进行预测
#     for image_file in image_files:
#         print(f"Predicting for image: {image_file}")
#         prediction_instance.predict_image_classification_sample(image_file)
