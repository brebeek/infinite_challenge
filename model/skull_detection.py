import http.client
import json
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials
from logger.base_logger import logger


# detect with azure.cognitiveservices API
def detect(img, prediction_key, conf, publish_iteration_name):
    ENDPOINT = 'https://skull-detection-sea.cognitiveservices.azure.com/'
    project_id = 'ae33224a-a67d-4489-bd07-a4405035700f'
    prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
    predictor = CustomVisionPredictionClient(ENDPOINT, prediction_credentials)
    logger.info('Requesting for skull detection')

    results = predictor.detect_image_with_no_store(project_id, publish_iteration_name, img)
    logger.info('Skull detection results retrieved')

    return interpret_result(results.predictions, conf)


def headers_with_prediction_key(key):
    assert len(key) > 0
    if len(key) == 0:
        raise ValueError('Prediction Key must be specified')
    return {
        # Request headers
        'Content-Type': 'application/octet-stream',
        'Prediction-key': key
    }


def detectHTTP(img, key, confidence, model_version):
    data = request_detection(img, model_version, key)
    boxes = interpret_result(data, confidence)
    return boxes


def request_detection(img, model_version, key):
    try:
        conn = http.client.HTTPSConnection('skull-detection-sea.cognitiveservices.azure.com')
        headers = headers_with_prediction_key(key)
        conn.request("POST", f'/customvision/v3.0/Prediction/ae33224a-a67d-4489-bd07-a4405035700f/detect/iterations/{model_version}/image', img, headers)
        response = conn.getresponse()
        data = response.read()
        data = json.loads(data)
        conn.close()
        return data
    except Exception as e:
        logger.critical("Error connecting to Cognitive Services:", e)
        raise e


def interpret_result(result, conf):
    boxes = []
    try:
        for detection in result:
            if detection.probability < conf:
                continue
            json_box = detection.bounding_box
            xywh_box = [json_box.left, json_box.top, json_box.width, json_box.height]
            boxes.append(xywh_to_yxyx(xywh_box))
        return boxes
    except Exception as e:
        logger.critical("Bad response:", e)
        raise e


def xywh_to_yxyx(orig_box):
    assert len(orig_box) == 4
    x2 = orig_box[0]
    x1 = x2 + orig_box[2]
    y1 = orig_box[1]
    y2 = y1 + orig_box[3]
    return [y1, x1, y2, x2]
