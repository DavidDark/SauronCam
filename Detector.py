#Librerías importadas para el correcto funcionamiento del Detector.
#Es necesario tenerlos instalados para poder importarlos
import imutils
import numpy as np
import cv2
import argparse
import time
from imutils.video import VideoStream

#Método para la definición de argumentos. Aquí se carga el modelo y el nivel de confianza para la detección.
def Arguments ():
    ap = argparse.ArgumentParser()
    #Están definidos en Default para eficientizar la corrida del programa.
    ap.add_argument("-p", "--prototxt", default="face_detection_model/deploy.prototxt.txt", help="path to Caffe 'deploy' prototxt file")
    ap.add_argument("-m", "--model", default="face_detection_model/res10_300x300_ssd_iter_140000.caffemodel",help="path to Caffe pre-trained model")
    ap.add_argument("-c", "--confidence", type=float, default=0.5, help="minimum probability to filter weak detections")
    args = vars(ap.parse_args())
    #El Modelo que se está usando es el de CAFFE que incluye OpenCV para la detección facial.
    print("[INFO] Cargando modelo de Deteccion CAFFE...")
    net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])
    return(args,net)
#Método para la detección Facial. Que recibe los argumentos obtenidos por el método anterior.
def Detectar(vs, args, net):

    #Toma un frame del stream y le cambia el tamaño aun máximo de 1000 pixeles de ancho
    frame = vs.read()
    frame = imutils.resize(frame, width=1000, height=1000)

    #Toma las dimensiones del frame y lo transforma en un blob para su edición
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300), (103.93, 116.77, 123.68))

    # Pasa el blob atráves de la network y obtiene las detecciones y las predicciones
    net.setInput(blob)
    detections = net.forward()
        
    for i in range(0, detections.shape[2]):
        # Extrae la confianza (probabilidad) asosciada con la predicción.
        confidence = detections[0, 0, i, 2]

        # Filtra las detecciones débiles asegurandose que la confianza es mayor al nivel mínimo de confianza
        # que definimos en los argumentos.
        if confidence < args["confidence"]:
            continue

        # Computa las coordenadas (x, y) en los bordes de la caja a dibujar alrededor del objeto.
        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
        (startX, startY, endX, endY) = box.astype("int")

        # Dibuja la caja en conjunto con la probabilidad del objeto detectado como un rostro.
        #text = "{:.2f}%".format(confidence * 100)
        #y = startY - 10 if startY - 10 > 10 else startY + 10
        #cv2.rectangle(frame, (startX, startY), (endX, endY),
        #                (0, 0, 255), 2)
        #cv2.putText(frame, text, (startX, y),
        #    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

    return(frame) 
#Método para Isolated test.
#Este fragmento de código sirve para correr esta clase de forma individual.
if __name__ == "__main__":
    print("[INFO] Iniciando prueba del Detector, porfavor espere...")
    vs = VideoStream(src=0).start()
    time.sleep(3)

    args,net = Arguments()
    while True:
        frame = Detectar(vs,args,net)
        key = cv2.waitKey(1) & 0xFF
        cv2.imshow("Detector Facial de Registro", frame)
    
    # Presiona la tecla '*' para terminar el loop
        if key == ord("*"):
            cv2.destroyAllWindows()
            vs.stop()
            print("[INFO] Cerrando Detector.")
            break