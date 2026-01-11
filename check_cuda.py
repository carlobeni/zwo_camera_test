#!/usr/bin/env python3
import torch
from ultralytics import YOLO
import cv2

print("Torch version:", torch.__version__)
print("CUDA available:", torch.cuda.is_available())
print("GPU:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "NO GPU")

model = YOLO("yolov8n.pt")
model.to("cuda")

print("YOLO cargado en CUDA correctamente")