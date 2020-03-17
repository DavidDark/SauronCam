import tkinter as tk
from PIL import ImageTk, Image
import os
import time

def imprime():
    print("Hola!")

DIRECTORY = "assets"

def getImage(path):
    try:
        temp_img = ImageTk.PhotoImage(Image.open(path).resize((250, 250), Image.ANTIALIAS))
        return temp_img
    except:
        
        temp_img = ImageTk.PhotoImage(Image.open("assets/Sackboy.jpg"))
        return temp_img

def getInfo(path):
    #return ["NOMBRE", "APELLIDO", "CUMPLEAÑOS", "CONTACTO", "SUPERVISOR", "COMENTARIOS"]
    try:
        file_object = open(r"logdetection/log.txt", "r")
        name = file_object.readline()
        lastname = file_object.readline()
        bday = file_object.readline()
        contact = file_object.readline()
        supervirsor = file_object.readline()
        coments = file_object.readline()
        file_object.close()
        return [name, lastname, bday, contact, supervirsor, coments]
    except:
        return ["NOMBRE", "APELLIDO", "CUMPLEAÑOS", "CONTACTO", "SUPERVISOR", "COMENTARIOS"]

def didChange(x):
    return True

class GUI(tk.Frame):
    #Creating main window
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Ultima deteccion POI")
        self.master.geometry("500x400")
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.ejemplo = tk.Button(self, padx = 50, pady = 10)
        self.ejemplo["text"] = "Ejemplo"
        self.ejemplo["command"] = imprime
        #self.ejemplo.grid(row = 0, column = 0, columnspan = 2, padx = 20, pady = 10)


        self.image_show = getImage("assets/Sackboy.jpg")

        self.snap = tk.Label(self, image = self.image_show)
        self.snap.grid(row = 0, column = 0, columnspan = 1, rowspan = 5)

        self.name = tk.Label(self, text = "Nombre: ", anchor = "w")
        self.name.grid(row = 0, column = 1)

        self.lastname = tk.Label(self, text = "Apellido: ", anchor = "w")
        self.lastname.grid(row = 1, column = 1)

        self.bday = tk.Label(self, text = "Fecha de nacimiento: ", anchor = "w")
        self.bday.grid(row = 2, column = 1)

        self.contact = tk.Label(self, text = "Contacto: ", anchor = "w")
        self.contact.grid(row = 3, column = 1)

        self.supervirsor = tk.Label(self, text = "Supervisor: ", anchor = "w")
        self.supervirsor.grid(row = 4, column = 1)

        self.comentarios = tk.Label(self, text = "Comentarios: ", anchor = "w")
        self.comentarios.grid(row = 5, column = 0)

        ######
        self.nameT = tk.Label(self, text = "nnnnnnnnnnn", anchor = "w")
        self.nameT.grid(row = 0, column = 2)

        self.lastnameT = tk.Label(self, text = "aaaaaaaa", anchor = "w")
        self.lastnameT.grid(row = 1, column = 2)

        self.bdayT = tk.Label(self, text = "dd/mm/aaaa", anchor = "w")
        self.bdayT.grid(row = 2, column = 2)

        self.contactT = tk.Label(self, text = "844XXXXXXX", anchor = "w")
        self.contactT.grid(row = 3, column = 2)

        self.supervirsorT = tk.Label(self, text = "ssssssssss", anchor = "w")
        self.supervirsorT.grid(row = 4, column = 2)

        self.comentariosT = tk.Label(self, text = "pppppppppppppppppppp pppppppppppppppppppp, pppppppppp\nppppppppppppppp", anchor = "w")
        self.comentariosT.grid(row = 6, column = 0,  columnspan = 2)

        self.change = True

        self.after(10, self.updates)

    def updates(self):
        if(didChange(self.change)):
            self.inf = getInfo("TODO")
            self.change = False
            self.image_show = getImage("logdetection/lastsnap.jpg")
            if self.image_show is "-1":
                self.after(100, self.updates)
            self.snap["image"] = self.image_show
            self.nameT['text'] = self.inf[0]
            self.lastnameT['text'] = self.inf[1]
            self.bdayT['text'] = self.inf[2]
            self.contactT['text'] = self.inf[3]
            self.supervirsorT['text'] = self.inf[4]
            self.comentariosT['text'] = self.inf[5]


        self.after(50, self.updates)

def main():
    root = tk.Tk()
    app = GUI(master = root)
    app.mainloop()

if __name__ == '__main__':
    main()
