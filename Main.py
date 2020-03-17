#Se importan las clases principales
import Registro as reg
import Reconocimiento as rec
import tkinter as tk

#A user interface that manages the options of the program
class GUI(tk.Frame):

	#Creatung main window
	def __init__(self, master = None):
		super().__init__(master)
		self.master = master
		self.master.title("FARDER AIM")
		self.master.geometry("250x130")
		self.pack()
		self.create_widgets()


	def create_widgets(self):
		#Registrar
		self.registrar = tk.Button(self, padx = 52, pady = 10)
		self.registrar["text"] = "Registrar"
		self.registrar["command"] = reg.Registrar
		self.registrar.pack(side = "top")

		#Reconocimiento facial
		self.reconocer = tk.Button(self, pady = 10)
		self.reconocer["text"] = "Reconocimiento facial"
		self.reconocer["command"] = rec.Reconocer
		self.reconocer.pack(side = "top")

		#Salir
		self.salir = tk.Button(self, text = "Salir", fg = "red", command =self.master.destroy, padx = 70, pady = 10)
		self.salir.pack(side = "bottom")


def main():
	#Calling the GUI
	root = tk.Tk()
	app = GUI(master = root)
	app.mainloop()

if __name__ == '__main__':
	main()

#En un pequeño menù dentro de la consola se muestran las clases ligadas que se pueden ejecutar
#Se remplazo por el GUI                       
while(False):
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
