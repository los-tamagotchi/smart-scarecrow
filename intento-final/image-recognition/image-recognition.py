from tkinter import *
from PIL import Image, ImageTk #pip install Pillow
import cv2 # pip install opencv-contrib-python
from ultralytics import YOLO #pip install ultralytics
from ultralytics.utils.plotting import Annotator
from pyModbusTCP.client import ModbusClient
#https://docs.ultralytics.com/reference/utils/plotting/#ultralytics.utils.plotting.Annotator

import numpy as np

#CONECTION
SERVER_HOST = "192.168.195.99"
SERVER_PORT = 502
CAMERA_COIL = 0

client = ModbusClient(host= SERVER_HOST, port=SERVER_PORT, auto_open=True, debug=False)


def onClossing():
    root.quit()         #finaliza este programa
    cap.release()
    root.destroy()      #Cierra la ventana creada


def callback():

        cap.open(url) # Antes de capturar el frame abrimos la url

        ret, frame = cap.read()

        if ret:

            results = model.predict(frame, stream=True,verbose=False)

            for result in results:
                boxes = result.boxes
                #annotator = Annotator(frame)

                for box in boxes:
                    r = box.xyxy[0]
                    c = box.cls
                    if classes[int(c)] == "pajaro":
                        client.write_single_coil(CAMERA_COIL, 1)
                        print("¡Detectado!")
                        #annotator.box_label(r, label=classes[int(c)],color=COLORS[int(c)])
                    else:
                        client.write_single_coil(CAMERA_COIL, 0)




            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            #img.thumbnail((800,800)) #Redimensionar imagen
            #tkimage = ImageTk.PhotoImage(img)
            #label.configure(image = tkimage )
            #label.image = tkimage


            root.after(1,callback)
            client.write_single_coil(CAMERA_COIL, 0)

        else:
            onClossing()

model = YOLO("yolov8n.pt")

classesFile = "C:/Users/eduda/Desktop/pigeon-repeller/intento-final/image-recognition/coco.names"
with open(classesFile, 'rt') as f:
    classes = f.read().rstrip('\n').split('\n')
    COLORS = np.random.uniform(0, 255, size=(len(classes),3))

url='http://192.168.195.188/480x320.jpg'
cap = cv2.VideoCapture(url) # Crear objeto VideoCapture


if cap.isOpened():
    print("Cámara iniciada")
else:
    sys.exit("Cámara desconectada")

############################## HMI design #################
root = Tk()
root.protocol("WM_DELETE_WINDOW",onClossing)
root.title("Vision Artificial") # titulo de la ventana

label=Label(root) #image = imagen camara opencv / relief = decoracion de borde
label.grid(row=1,padx=20,pady=20)

root.after(1,callback) #Es un método definido para todos los widgets tkinter.
root.mainloop()
