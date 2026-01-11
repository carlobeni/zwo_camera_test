#!/usr/bin/env python3
import os
import cv2
import numpy as np
import time
from ultralytics import YOLO
import zwoasi as asi

# --------------------------------------------------
# 1) Inicializar SDK ZWO
# --------------------------------------------------
asi.init(os.environ["ZWO_ASI_LIB"])

# --------------------------------------------------
# 2) Detectar cámaras
# --------------------------------------------------
n = asi.get_num_cameras()
if n == 0:
    raise RuntimeError("No se detecta ninguna ASI. Revisa USB/udev/permisos.")

print("Cámaras detectadas:", n)

cam = asi.Camera(0)

# --------------------------------------------------
# 3) Configuración de cámara
# --------------------------------------------------
WIDTH  = 640
HEIGHT = 480
BIN    = 1

cam.set_image_type(asi.ASI_IMG_RAW8)
cam.set_roi_format(WIDTH, HEIGHT, BIN, asi.ASI_IMG_RAW8)

EXPOSURE_US = 10000   # 10 ms
GAIN = 50

cam.set_control_value(asi.ASI_EXPOSURE, EXPOSURE_US)
cam.set_control_value(asi.ASI_GAIN, GAIN)

# --------------------------------------------------
# 4) Iniciar captura de video
# --------------------------------------------------
cam.start_video_capture()
print("Captura de video iniciada")

TIMEOUT_MS = int(EXPOSURE_US / 1000 * 2 + 500)

# --------------------------------------------------
# 5) Cargar YOLO (CUDA)
# --------------------------------------------------
model = YOLO("yolov8n.pt")
model.to("cuda")

# --------------------------------------------------
# 6) FPS robusto (ventana temporal)
# --------------------------------------------------
fps_window = 30
frame_count = 0
t0 = time.perf_counter()
fps = 0.0

# --------------------------------------------------
# 7) Loop principal
# --------------------------------------------------
try:
    while True:
        try:
            frame = cam.capture_video_frame(timeout=TIMEOUT_MS)
        except asi.ZWO_IOError:
            continue

        if frame is None:
            continue

        # ---------- FPS ----------
        frame_count += 1
        if frame_count == fps_window:
            t1 = time.perf_counter()
            fps = fps_window / (t1 - t0)
            t0 = t1
            frame_count = 0

        # ---------- Imagen ----------
        img_gray = frame.reshape((HEIGHT, WIDTH))
        img_bgr  = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2BGR)

        # ---------- YOLO ----------
        results = model(img_bgr, device="cuda", verbose=False)
        annotated = results[0].plot()

        # ---------- Overlay FPS ----------
        cv2.putText(
            annotated,
            f"FPS: {fps:5.1f}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (0, 255, 0),
            2,
            cv2.LINE_AA
        )

        cv2.imshow("ASI174 + YOLO (CUDA) + FPS", annotated)

        if cv2.waitKey(1) & 0xFF == 27:
            break

# --------------------------------------------------
# 8) Cierre limpio
# --------------------------------------------------
finally:
    cam.stop_video_capture()
    cam.close()
    cv2.destroyAllWindows()
    print("Cámara cerrada correctamente")
