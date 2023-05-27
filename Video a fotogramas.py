import cv2
import os
import time
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter.ttk import Progressbar

def printtoconsole(text):
    console_text.config(state=tk.NORMAL)
    console_text.insert(tk.END, text + '\n')
    console_text.config(state=tk.DISABLED)
    console_text.see(tk.END)

def split_video_frames(video_path, output_folder):
    printtoconsole(f"Procesando video: {video_path}")

    # Verificar si el archivo de video existe
    if not os.path.isfile(video_path):
        messagebox.showerror("Error", f"El archivo de video '{video_path}' no existe.")
        return

    # Crear la subcarpeta si no existe
    if not os.path.exists(output_folder):
        try:
            os.makedirs(output_folder)
        except OSError as e:
            messagebox.showerror("Error", f"No se pudo crear la carpeta de salida '{output_folder}': {e}")
            return

    # Cargar el video
    video = cv2.VideoCapture(video_path)
    if not video.isOpened():
        messagebox.showerror("Error", "No se pudo abrir el archivo de video.")
        return

    success, image = video.read()
    count = 0
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    # Configurar la barra de progreso
    progress_bar["maximum"] = total_frames

    # Iterar sobre los fotogramas del video
    while success:
        # Guardar el fotograma actual como archivo JPG
        frame_path = os.path.join(output_folder, f"frame_{count}.jpg")
        cv2.imwrite(frame_path, image)

        # Imprimir el mensaje por cada imagen procesada y exportada
        printtoconsole(f"Imagen procesada y exportada: {frame_path}")

        # Actualizar la barra de progreso
        progress_bar["value"] = count + 1
        window.update_idletasks()
        window.update()

        # Leer el siguiente fotograma
        success, image = video.read()
        count += 1

    # Liberar el video
    video.release()

    printtoconsole(f"Procesamiento completado para el video: {video_path}")
    return count

def choose_video_files():
    archivos = filedialog.askopenfilenames(filetypes=[("Archivos de video", "*.mp4;*.avi")])
    if archivos:
        video_entry.delete(0, tk.END)
        video_entry.insert(0, ", ".join(archivos))
        convert_button.config(state="normal")


        # Establecer la carpeta de salida predeterminada
        carpeta_salida = os.path.dirname(archivos[0])
        carpeta_salida_default = f"{os.path.basename(carpeta_salida)}_frames"
        output_entry.delete(0, tk.END)
        output_entry.insert(0, os.path.join(carpeta_salida, carpeta_salida_default))

def choose_output_folder():
    carpeta = filedialog.askdirectory()
    if carpeta:
        output_entry.delete(0, tk.END)
        output_entry.insert(0, carpeta)

def convert_videos():
    printtoconsole("por Bondaz Pablo")
    archivos = video_entry.get().split(", ")
    carpeta_salida = output_entry.get()
    total_videos = len(archivos)

    videos_procesados = []
    window.update()
    fotogramas_extraidos = []
    time.sleep(0.6)
    for archivo in archivos:
        output_folder = os.path.join(carpeta_salida, os.path.splitext(os.path.basename(archivo))[0])
        fotogramas = split_video_frames(archivo, output_folder)
        videos_procesados.append(archivo)
        fotogramas_extraidos.append(fotogramas)

    messagebox.showinfo("Proceso completado", f"Proceso completado para {total_videos} video(s).\n\nVideos procesados:\n{', '.join(videos_procesados)}\n\nFotogramas extraídos:\n{', '.join(map(str, fotogramas_extraidos))}")

# Crear la ventana principal
window = tk.Tk()
window.title("Video a fotogramas")
window.geometry("400x380")
window.resizable(False, False)
window.iconbitmap("C:/Users/pablo/Downloads/icono-video-a-fotogramas.ico")

# Etiqueta y cuadro de texto para elegir los archivos de video
video_label = tk.Label(window, text="Archivos de Video:")
video_label.pack()
video_entry = tk.Entry(window, width=50)
video_entry.pack()

# Botón para elegir los archivos de video
video_button = tk.Button(window, text="Seleccionar Video(s)", command=choose_video_files)
video_button.pack()

# Etiqueta y cuadro de texto para elegir la carpeta de salida
output_label = tk.Label(window, text="Carpeta de Salida:")
output_label.pack()
output_entry = tk.Entry(window, width=50)
output_entry.pack()

# Botón para elegir la carpeta de salida
output_button = tk.Button(window, text="Seleccionar Carpeta", command=choose_output_folder)
output_button.pack()

# Botón para convertir los videos
convert_button = tk.Button(window, text="Convertir", command=convert_videos)
convert_button.config(state="disabled")
convert_button.pack()

# Barra de progreso
progress_bar = Progressbar(window, orient=tk.HORIZONTAL, length=200, mode='determinate')


progress_bar.pack()

# Cuadro de texto de la consola
console_text = tk.Text(window, state=tk.DISABLED, height=10, width=50)
console_text.pack()

# Redirigir la salida estándar a la consola
import sys
class ConsoleRedirector:
    def __init__(self, console_text_widget):
        self.console_text_widget = console_text_widget

    def write(self, text):
        self.console_text_widget.config(state=tk.NORMAL)
        self.console_text_widget.insert(tk.END, text)
        self.console_text_widget.config(state=tk.DISABLED)
        self.console_text_widget.see(tk.END)

sys.stdout = ConsoleRedirector(console_text)

# Iniciar el bucle de eventos de la ventana
window.mainloop()
