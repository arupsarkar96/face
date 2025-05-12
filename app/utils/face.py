import cv2
import numpy as np
from deepface import DeepFace
import os

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"


def get_embedding(image_path):
    try:
        result = DeepFace.represent(img_path=image_path, model_name="Facenet", enforce_detection=False)
        if result and len(result) > 0:
            return np.array(result[0]["embedding"], dtype=np.float32)
        return None
    except Exception as e:
        print("Error extracting embedding:", str(e))
        return None