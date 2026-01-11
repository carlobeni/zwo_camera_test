#!/usr/bin/env python3
import zwoasi as asi
import os
import time

asi.init(os.environ["ZWO_ASI_LIB"])

print("Detectando cámaras...")
n = asi.get_num_cameras()
print("Cámaras detectadas:", n)

if n == 0:
    exit(0)

time.sleep(0.2)
cam = asi.Camera(0)

info = cam.get_camera_property()
print("Información de la cámara:")
for k, v in info.items():
    print(f"  {k}: {v}")

cam.close()
print("Cámara cerrada correctamente")
