#Se importa una librería para entrenar el modelo, esta es sklearn
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
import argparse
import pickle

def EArgs():
	#Método para la definición de argumentos. Aquí se cargan los archivos .pickle para entrenar el modelo.
	ap = argparse.ArgumentParser()
	ap.add_argument("-e", "--embeddings", default="output/embeddings.pickle",
		help="path to serialized db of facial embeddings")
	ap.add_argument("-r", "--recognizer", default="output/recognizer.pickle",
		help="path to output model trained to recognize faces")
	ap.add_argument("-l", "--le", default="output/le.pickle",
		help="path to output label encoder")
	args = vars(ap.parse_args())
	return(args)

def Entrenar(args):
	# Carga los rostros identificados
	print("[INFO] Loading face embeddings...")
	data = pickle.loads(open(args["embeddings"], "rb").read())

	# Codifica los nombres como labels
	print("[INFO] Encoding labels...")
	le = LabelEncoder()
	labels = le.fit_transform(data["names"])

	# Entrena el modelo en base a los 128-d puntos del rostro que se utilizan para el reconocimiento
	#Después es que realiza el recnonocimiento
	print("[INFO] Training model...")
	recognizer = SVC(C=1.0, kernel="linear", probability=True)
	recognizer.fit(data["embeddings"], labels)

	# Escribe los datos obtenidos del reconocimiento en disco. Sobre el archivo pickle.
	f = open(args["recognizer"], "wb")
	f.write(pickle.dumps(recognizer))
	f.close()

	# Escribe el codificado de los nombres en disco
	f = open(args["le"], "wb")
	f.write(pickle.dumps(le))
	f.close()