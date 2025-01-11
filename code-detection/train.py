from ultralytics import YOLO

model = YOLO("yolo11n-seg.pt")

results = model.train(
    data="data.yaml",
    epochs=50,
    imgsz=640,
    batch=-1,
    cache=True,
    device=0,
    lr0=0.01,
    lrf=0.005,
    close_mosaic=10,
)
