#Clases importadas
import Args_Recog
# Librerías importadas para el reconocimiento en tiempo real a través de la cámara web
#Recuerda tener la cámara web utilizable si estás en una máquina virtual, desde la pestaña de dispositivos
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import imutils
import pickle
import time
import cv2
import os
#SQLITE
#import sqlite3
#from sqlite3 import Error
#def connection(db_file):
#	conn = None
#	try:
#		conn = sqlite3.connect(db_file)
#	except Error as e:
#		print(e)
#	return conn

#def select(conn):
#	cur = conn.cursor()
#	cur.execute("SELECT * FROM Registro")
#	rows = cur.fetchall()
#	for row in rows:
#		print(row)

def Reconocer():
#	database = r"Miembros.db"
#	conn = connection(database)

	#Se manda a llamar el método con los argumentos por defecto para el reconocimiento de Video
	args= Args_Recog.ArgsV()

	# Se asignan los modelos de detección con su respectiva dirección
	print("[INFO] Cargando detector...")
	protoPath = os.path.sep.join([args["detector"], "deploy.prototxt"])
	modelPath = os.path.sep.join([args["detector"],
		"res10_300x300_ssd_iter_140000.caffemodel"])
	detector = cv2.dnn.readNetFromCaffe(protoPath, modelPath)

	# Se asigna el modelo de asignación para el reconocimiento facial
	print("[INFO] Cargando Reconocimiento Facial...")
	embedder = cv2.dnn.readNetFromTorch(args["embedding_model"])

	# Se ejecuta el modelo de reconocimiento facial.
	recognizer = pickle.loads(open(args["recognizer"], "rb").read())
	le = pickle.loads(open(args["le"], "rb").read())

	# Se inicia el stream de video al activar la cámara web
	print("[INFO] Iniciando Stream de video...")
	vs = VideoStream(src=0).start()
	time.sleep(2.0)

	# Se inicia tambien la variable para mostrar los FPS durante la ejecución
	fps = FPS().start()

	print("[INFO] Presiona * para salir.")
	# Se ejecuta un ciclo a través de los frames extraídos del stream
	framming = 0

	while True:
		# Se obtiene un frame del stream
		frame = vs.read()
		#Redimensiona el frame obtenido a un ancho de 600 pixeles, manteniendo el aspect ratio
		# Después toma las dimensiones de imágen
		frame = imutils.resize(frame, width=600)
		(h, w) = frame.shape[:2]

		# Construye un blob a partir del frame
		imageBlob = cv2.dnn.blobFromImage(
			cv2.resize(frame, (300, 300)), 1.0, (300, 300),
			(104.0, 177.0, 123.0), swapRB=False, crop=False)

		# Aplica el DETECTOR FACIAL BASADO EN DEEP LEARNING DE OPENCV en la imágen introducida
		detector.setInput(imageBlob)
		detections = detector.forward()

		# Lleva a cabo un ciclo de acuerdo a las detecciones.
		for i in range(0, detections.shape[2]):
			# Extrae el nivel de confianza (probabilidad) de acuerdo a las predicciones
			confidence = detections[0, 0, i, 2]

			# Filtra las detecciones debiles
			if confidence > args["confidence"]:
				# Computa las coordenadas (x,y) para dibujar una caja alrededor de los rostros detectados
				box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
				(startX, startY, endX, endY) = box.astype("int")

				# Extrae el Face ROI
				face = frame[startY:endY, startX:endX]
				(fH, fW) = face.shape[:2]

				# Se asegura que el largo y ancho de la cara sean lo suficientemente grandes
				if fW < 20 or fH < 20:
					continue

				#Construye un blob para el face ROI, para después pasarlo por el modelo de asignación
				# para obtener las 128-d cuantificaciones de la cara
				faceBlob = cv2.dnn.blobFromImage(face, 1.0 / 255,
					(96, 96), (0, 0, 0), swapRB=True, crop=False)
				embedder.setInput(faceBlob)
				vec = embedder.forward()

				# Ejecuta el reconocimiento de la cara. Otorgandonos una probabilidad.
				preds = recognizer.predict_proba(vec)[0]
				j = np.argmax(preds)
				proba = preds[j]
				name = le.classes_[j]

				# Dibuja la cara alrededor del rostro detectado, junto con la probabilidad del reconocimiento.
				text = "{}: {:.2f}%".format(name, proba * 100)
				y = startY - 10 if startY - 10 > 10 else startY + 10
				cv2.rectangle(frame, (startX, startY), (endX, endY),(0, 0, 255), 2)

				#T es un valor asignado a un estandar de probabilidad para determinar si es conocido o no.
				T=0.90

				if proba > T:
					cv2.rectangle(frame, (startX, startY), (endX, endY),(0, 0, 255), 2)
					#Si la probabilidad es mayor al estandar, entonces se escribe el nombre y la probabilidad asignadas
					#respecto al proceso de reconocimiento.
					cv2.putText(frame, text, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
					
				else:
					cv2.rectangle(frame, (startX, startY), (endX, endY),(0, 0, 255), 2)
					#Si la probabilidad es menor al estandar asignado, se escribe el nombre de desconocido y su probabilidad.
					cv2.putText(frame,"cliente: {:.2f}%".format(proba * 100),(startX, y),cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0,0,255),2)
				
				
				if name == "Diego":
					framming += 1
					if framming > 20:
						cv2.rectangle(frame, (startX, startY), (endX, endY),(0, 0, 255), 2)
						print("Es Diego Flores, posible ladrón de sonrisas, favor de vigilar.")
						#select(conn)

						framming = 0
					else:
						continue
				else:
					framming = 0
					continue
					

		# Actualiza el contador de los FPS
		fps.update()

		# Muestra el frame obtenido
		cv2.imshow("Frame", frame)
		key = cv2.waitKey(1) & 0xFF

		# Si presiona la tecla "*" se detiene el ciclo de detección y reconocimiento.
		if key == ord("*"):
			break

	# Detiene el temporizador y muestra la última información de los FPS
	fps.stop()
	print("[INFO] Tiempo de ejecución: {:.2f}".format(fps.elapsed()))
	print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

	# Cierra la ventana y los procesos.
	cv2.destroyAllWindows()
	vs.stop()