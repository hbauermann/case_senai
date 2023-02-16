from datetime import datetime
import uuid
import requests
import cv2
from ultralytics import YOLO
import base64
import pandas as pd
import numpy as np


def login_api(url, username, password):
    login = {
        "username": username,
        "password": password
    }
    login_to_db = requests.post(url, json=login)
    if login_to_db.status_code == 401:
        print('Não autorizado')
        return {
            "refresh": "",
            "access": ""
        }
    else:
        return login_to_db.json()


def send_to_db(url, mac, classification, evidence, token):
    result = {
        "mac": mac,
        "date": str(datetime.now()),
        "classification": classification,
        "evidence": evidence
    }
    header = {"Authorization": ("Bearer " + token)}
    send_to_db = requests.post(url, headers=header, json=result)
    return send_to_db.status_code


def renew_token(url, refresh_token):
    refresh = {
        "refresh": refresh_token
    }
    new_token = requests.post(url, json=refresh)
    return new_token.json()


def convert_to_b64(img_to_convert):
    base64_image = base64.b64encode(
        cv2.imencode('.png', img_to_convert)[1]).decode()
    return base64_image


def yolov8_mouse_detect(image_souce, model_to_use):
    list_of_results = []
    list_of_detection = []
    predict_result = model_to_use(source=image_souce)
    for result in predict_result:
        list_of_results.append(result.boxes)
    for a in list_of_results:
        for b in a:
            if b.cls == 64 and b.conf >= 0.7:
                for (x, y, x1, y1) in b.xyxy:
                    x = int(x)
                    y = int(y)
                    x1 = int(x1)
                    y1 = int(y1)
                    list_of_detection.append([x, y, x1, y1])
    return list_of_detection


def cut_detection(list_of_results, image_to_cut):
    #list_of_images = []
    dist = 10
    for (x, y, x1, y1) in list_of_results:
        x = int(x)
        y = int(y)
        x1 = int(x1)
        y1 = int(y1)
        #list_of_images.append(image_to_cut[y-dist:y1+dist, x-dist:x1+dist])
        image = image_to_cut[y-dist:y1+dist, x-dist:x1+dist]
    return image


if __name__ == "__main__":
    image_souce_cv2 = cv2.imread('testes_imagens\\3.png')
    #model = YOLO("runs\\detect\\yolov8n_custom9\\weights\\best.pt") #modelo do treinamento (não ficou bom).
    model = YOLO('yolov8n.pt')

    date_oc = str(datetime.now())
    mac_oc = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff)
                       for ele in range(0, 8*6, 8)][::-1]).upper()
    class_oc = 'MOUSE'
    url_detection_db = 'http://localhost:8000/detection/'
    login_url = 'http://localhost:8000/api/autentication/login'
    renew_url = 'http://localhost:8000/api/autentication/renovate'

    username = 'admin' 
    password = 'Senai@2023' #pode ser colocada como variável de ambiente

    positive_detection = yolov8_mouse_detect(image_souce_cv2, model)
    if len(positive_detection) != 0:
        imagem_detectada = cut_detection(positive_detection, image_souce_cv2)
        imagem_detectada_b64 = convert_to_b64(imagem_detectada)
        token = login_api(login_url, username, password)
        access_token = token['access']
        #refresh_token = token['refresh']
        send_to_db_data = send_to_db(
            url_detection_db, mac_oc, class_oc, imagem_detectada_b64, access_token)
        print(send_to_db_data)

    """
    Para detectar via webcam - EM TESTES
    vid = cv2.VideoCapture(0)
    while(True):
        ret, frame = vid.read()
        cv2.imshow('frame', frame)
        detection = yolov8_mouse_detect(frame, model)
        print(detection)
        if len(detection) != 0:
            positive_det = cut_detection(yolov8_mouse_detect(image_souce_cv2, model), image_souce_cv2)
            cv2.imwrite('positive_det.png', positive_det)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    vid.release()
    cv2.destroyAllWindows()
    """
