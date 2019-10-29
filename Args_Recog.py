#Este es un método para definir los argumentos default de las clases para el reconocimiento.
import argparse

def ArgsV():
	# Constructor para los argumentos utilizados.
	#Entre los argumentos se encuentra el modelo y los archivos variables tipo pickle en output.
	#Desafortunadamente no parece haber manera de editar este último tipo de archivos, es necesario
	#investigarlos más a fondo. De ser posible.
	ap = argparse.ArgumentParser()
	ap.add_argument("-d", "--detector", default="face_detection_model",
		help="path to OpenCV's deep learning face detector")
	ap.add_argument("-m", "--embedding-model", default="openface_nn4.small2.v1.t7",
		help="path to OpenCV's deep learning face embedding model")
	ap.add_argument("-r", "--recognizer", default="output/recognizer.pickle",
		help="path to model trained to recognize faces")
	ap.add_argument("-l", "--le", default="output/le.pickle",
		help="path to label encoder")
	ap.add_argument("-c", "--confidence", type=float, default=0.7,
		help="minimum probability to filter weak detections")
	args = vars(ap.parse_args())
	return(args)