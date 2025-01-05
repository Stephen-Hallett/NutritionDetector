import cv2 as cv
from ultralytics import YOLO

model = YOLO("runs/segment/train5/weights/best.pt")

img = cv.imread("test_img2.jpg")

results = model(img)
result = results[0]
result.save(filename="result.jpg")
