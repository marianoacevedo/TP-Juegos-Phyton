import tkinter as tk # Tkinter es la biblioteca estándar de Python utilizada para crear interfaces gráficas de usuario (GUI). 
from tkinter import PhotoImage
import subprocess # Importa el modulo subprocess que Permite ejecutar programas y scripts externos desde dentro de un programa Python.
import pygame
 
def start_game_from_image(game_file):

    subprocess.Popen(['python', game_file])   # Ejecuta el archivo del juego
    pygame.mixer.music.load("sound/rap_2.wav")
    pygame.mixer.music.play()
       

def create_game_menu(): # Funcion que crea el menu de los juegos

    pygame.init()
    pygame.mixer.music.load("sound/rap_8.wav")
    pygame.mixer.music.play()
    pygame.mixer.music.get_volume()
    pygame.mixer.music.set_volume(0.2)

    def exit_game():
        root.destroy()  # Cierra el menu principal
   

    root = tk.Tk()
    root.title("Menú de Juegos") #Titulo de la ventana
    root.geometry("1280x720") #Resolucion de pantalla
    root.iconbitmap("menu/video-game-play-pad-boy-gameboy-nintendo_108539.ico") #favicom

    # Centra los botones en la pantalla
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_position = int((screen_width - root.winfo_reqwidth()) / 2)
    y_position = int((screen_height - root.winfo_reqheight()) / 2)
    root.geometry("+{}+{}".format(x_position, y_position))
    
    background_image = PhotoImage(file="menu/fondo-pantalla.png") #Imagen del fondo de pantalla

    # Etiqueta para la imagen de fondo
    background_label = tk.Label(root, image=background_image)
    background_label.place(relwidth=1, relheight=1)

    road_fighter_image = PhotoImage(file="menu/road-fighter.png") #Imagenes de los botones de acceso a los juegos
    flappy_image = PhotoImage(file="menu/flappy-bird-android-7.png")
    
    #Etiqueta para los botones 
    road_fighter_button = tk.Button(root, image=road_fighter_image, width=426, height=240, command=lambda file="play.py": start_game_from_image(file))
    road_fighter_button.pack(pady=20)           
    
    flappy_button = tk.Button(root, image=flappy_image, width=426, height=240, command=lambda file="flappy.py": start_game_from_image(file))
    flappy_button.pack(pady=20)

    exit_button = tk.Button(root, text="Salir", command=exit_game, width=40, height=2, bg="grey", font=("Arial", 12), fg="white") # Boton de salida
    exit_button.pack(pady=20)
    
    root.mainloop()

if __name__ == "__main__":
    create_game_menu()
    