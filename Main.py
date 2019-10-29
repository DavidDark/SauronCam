#Se importan las clases principales
import Registro as reg
import Reconocimiento as rec

#En un pequeño menù dentro de la consola se muestran las clases ligadas que se pueden ejecutar

while(True):
	print("¿Qué acción desea realizar?")
	d= int(input("Registrar = 1. \nReconocimiento Facial = 2. \nSalir = Any. \n "))

	if d == 1:
		reg.Registrar()
		continue

	if d == 2:
		rec.Reconocer()
		continue
	else:
		#Presiona cualquier otra wevada para salir.
		print("Saliendo...")
		break