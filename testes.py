from ultralytics import YOLO

model = YOLO('yolov8n.pt')
a = model.predict(
   source='testes_imagens/1.png',
   conf=0.25
)
print(a)