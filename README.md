## Crear entorno de desarrollo para ASI174 + YOLO
Crear entorno virtual de Python y activarlo:
```bash
python3 -m venv asi_env
source asi_env/bin/activate
```

## Instalar SDK de ZWO
1. Verificar la arquitectura de tu sistema:
```bash
uname -m
```
2. Descargar SDK de ZWO e instalar la version acorde a tu arquitectura:
```bash
cd ~/tesis/zwo_camera_test
wget -O ASI_Camera_SDK.zip "https://dl.zwoastro.com/software?app=DeveloperCameraSdk&platform=windows86&region=Overseas"
unzip ASI_Camera_SDK.zip
tar -xvjf ASI_linux_mac_SDK_V1.40.tar.bz2
```
Esto creará una carpeta `ASI_Camera_SDK` con el SDK de ZWO.
```bash
ASI_linux_mac_SDK_V1.40/
 ├── lib/
 │    ├── x64/
 │    │    └── libASICamera2.so # para laptop
 │    ├── armv8/
 │    └── armv7/
 ├── include/
 └── examples/
 ```
3. Instalar la librería de ZWO en tu sistema:
```bash
sudo cp ASI_Camera_SDK/lib/x64/libASICamera2.so /usr/local/lib/
sudo ldconfig
```

4. Agregar variable de entorno `ZWO_ASI_LIB` al entorno virtual permanente:
```bash
code ~/asi_env/bin/activate
```
Al final del script agregar
```bash
export ZWO_ASI_LIB=/usr/local/lib/libASICamera2.so
```

5. Correccion udev (Depende del dispositivo PI/laptop):
Ver si la camara es detectada:
```bash
lsusb | grep -i zwo
```
Correccion
```bash
sudo tee /etc/udev/rules.d/99-zwo.rules << 'EOF'
SUBSYSTEM=="usb", ATTR{idVendor}=="03c3", MODE="0666"
EOF
```
Aplicar reglas
```bash
sudo udevadm control --reload-rules
sudo udevadm trigger
```


6. Instalar dependencias de yolo:
```bash
pip install --upgrade pip
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
pip install zwoasi opencv-python ultralytics numpy

