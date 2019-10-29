#Clases importadas
import Detector
import JustTrain
#Librerías importadas
import os
from imutils.video import VideoStream
import imutils
import cv2
import time
import glob


def Registrar():
	nombre = input(str("[INFO] Introduzca el Nombre del sujeto: "))

	#Verifica si existe el Folder para almacenar el dataset
	if not os.path.exists("dataset/{}".format(nombre)):
		os.mkdir("dataset/{}".format(nombre))
		print("[INFO] Miembro Registrado.")

	#Inicia la captura de la cámara
	print("[INFO] Iniciando 'VideoStream', porfavor espere...")
	vs = VideoStream(src=0).start()
	time.sleep(3)

	#Variables de ejecución y comparación
	snap = len(glob.glob("dataset/{}/*.jpg".format(nombre)))
	args,net = Detector.Arguments()
	times = 0

	#Se inicia el detector de manera continua
	print("[INFO] Presiona + para tomar las 9 fotografías y * para salir.")
	while True:
		#Carga y muestra el Detector Facial
		frame = Detector.Detectar(vs,args,net)
		key = cv2.waitKey(1) & 0xFF
		cv2.imshow("Detector Facial de Registro", frame)
		

		# Presiona la tecla "+" para tomar la foto
		if key == ord("+"):
			shot = 0
			print("[INFO] Tomando Fotografías...")
			# Este For está programado para tomar nueve fotografías seguidas.
			for shoot in range(0,2):
				photo = 'dataset/{}/{}.jpg'.format(nombre,snap)
				cv2.imwrite(photo,frame)
				snap+=1
				print("[INFO] Fotografía {} capturada.".format(shoot))
				shoot+=1
			times+=1

		# Presiona la tecla '*' para terminar el loop
		if key == ord("*"):
			cv2.destroyAllWindows()
			vs.stop()
			break
		#El loop tambien termina una vez que se han tomado 9 sesiones de 9 fotografías.
		#Añadiendo un total de 81 fotografías al dataset del Miembro
		if times == 20:
			cv2.destroyAllWindows()
			vs.stop()
			break

	#----Operaciones para actualizar y re-entrenar el modelo. -----
	cont= int(input("[INFO] ¿ Desea actualizar el Modelo ?"+"\nEsto puede durar algunos minutos, dependiendo de la población del data set."+
			"\n Si= 1, No= Any:  "))
	if cont == 1:
		#Es necesario para el modelo que exista más de un sólo folder para comparar en la carpeta de los dataset.
		if (int(len(glob.glob("dataset/*")) > 1)):
			JustTrain.Jt()
		else:
			print("[INFO] Registre Más Miembros.")
	else:
		print("[INFO] Listo...")
