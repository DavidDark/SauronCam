#Este archivo .py sirve solo para entrenar los modelos en un dado caso que se quiera hacer pruebas.
#Las primeras dos clases estàn para agilizar la creacion y actualizaciòn del modelo
import pyximport; pyximport.install()
import extract_embeddings
import train_model
import time
import glob

def Jt():
	print("\n [INFO] Actualizando Modelo...")
	start = time.time()
	extract_embeddings.Embeddings()
	print("\n [INFO] Modelo Actualizado.")

	print("\n [INFO] Entrenando Modelo...")
	args1 = train_model.EArgs()
	train_model.Entrenar(args1)
	print("\n [INFO] Modelo Entrenado.")
	duration = time.time() - start
	print(duration)

#Fragmento de código para Isolated test.
if __name__ == "__main__":
	if (int(len(glob.glob("dataset/*")) > 1)):
		Jt()
	else:
		print("[INFO] Registre Más Miembros.")