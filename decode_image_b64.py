import cv2
import base64
import numpy as np

image_to_test = cv2.imread('teste.png')
base64_image = base64.b64encode(cv2.imencode('.png', image_to_test)[1]).decode()
texto = base64_image


image_to_verify = base64.b64decode(b64.b64_image)
png_as_np = np.frombuffer(image_to_verify, dtype=np.uint8)
image_to_verify_decoded = cv2.imdecode(png_as_np, flags=1)