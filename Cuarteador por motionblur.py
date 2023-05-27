import os
import time
import cv2
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

stop = False


def stop_process():
    global stop
    stop = True
    printtoconsole("Proceso detenido por el usuario")


def calcular_motion_blur(img):
    kernel_size = int(kernel_size_entry.get())
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    height, width = gray.shape[:2]
    roi_width = int(width * 0.5)
    roi_height = int(height * 0.5)
    roi_start_x = int(width * 0.25)
    roi_start_y = int(height * 0.25)
    roi_end_x = roi_start_x + roi_width
    roi_end_y = roi_start_y + roi_height

    roi_gray = gray[roi_start_y:roi_end_y, roi_start_x:roi_end_x]
    fm = cv2.Laplacian(roi_gray, cv2.CV_64F).var()
    return fm


def crear_directorio(path):
    if not os.path.exists(path):
        os.makedirs(path)


def printtoconsole(text):
    console_text.configure(state='normal')
    console_text.insert(tk.END, text + "\n")
    console_text.configure(state='disabled')
    console_text.see(tk.END)


def enable_widgets():
    folder_entry.config(state="normal")
    folder_button.config(state="normal")
    set_size_combobox.config(state="normal")
    kernel_size_entry.config(state="normal")
    process_button.config(state="normal")


def disable_widgets():
    folder_entry.config(state="disabled")
    folder_button.config(state="disabled")
    set_size_combobox.config(state="disabled")
    kernel_size_entry.config(state="disabled")
    process_button.config(state="disabled")


def procesar_imagenes():
    global stop

    carpeta = folder_path.get()
    set_size = set_size_var.get()
    kernel_size = int(kernel_size_entry.get())

    if not carpeta:
        messagebox.showerror("Error", "No se ha seleccionado ninguna carpeta.")
        return

    carpeta_buenas = os.path.join(carpeta, "buenas")
    carpeta_malas = os.path.join(carpeta, "malas")
    crear_directorio(carpeta_buenas)
    crear_directorio(carpeta_malas)

    imagenes = os.listdir(carpeta)
    grupos = [imagenes[i:i + set_size] for i in range(0, len(imagenes), set_size)]

    buenas = []
    malas = []

    total_imagenes = len(imagenes)
    procesadas = 0

    progress_bar["maximum"] = total_imagenes
    progress_bar["value"] = 0

    disable_widgets()
    stop_button.config(state="normal")

    imagen_mayor_blur = ""
    imagen_menor_blur = ""
    printtoconsole("por Pablo Bondaz")
    window.update()
    time.sleep(0.6)
    for grupo in grupos:
        if stop:
            break

        lista_motion_blur = []
        for imagen in grupo:
            if stop:
                break

            imagen_path = os.path.join(carpeta, imagen)
            if not os.path.isfile(imagen_path):
                
                continue
            img = cv2.imread(imagen_path)
            if img is None:
                
                continue
            motion_blur = calcular_motion_blur(img)
            lista_motion_blur.append((imagen, motion_blur))

            # Verificar si es la imagen con mayor motion_blur
            if imagen_mayor_blur == "" or motion_blur > lista_motion_blur[0][1]:
                imagen_mayor_blur = imagen

            # Verificar si es la imagen con menor motion_blur
            if imagen_menor_blur == "" or motion_blur < lista_motion_blur[0][1]:
                imagen_menor_blur = imagen

        best_image = max(lista_motion_blur, key=lambda x: x[1])[0]
        buenas.append(best_image)
        shutil.move(os.path.join(carpeta, best_image), os.path.join(carpeta_buenas, best_image))
        printtoconsole(f"{best_image} - buenas")

        for imagen, _ in lista_motion_blur:
            if imagen != best_image:
                malas.append(imagen)
                shutil.move(os.path.join(carpeta, imagen), os.path.join(carpeta_malas, imagen))
                printtoconsole(f"{imagen} - malas")

        procesadas += len(grupo)
        progress_bar["value"] = procesadas
        window.update()

    enable_widgets()
    stop_button.config(state="disabled")

    if not stop:
        printtoconsole(f"Proceso Completado, buenas: {len(buenas)}, Malas: {len(malas)}")
        printtoconsole(f"Imagen con mayor calidad: {imagen_mayor_blur}")
        printtoconsole(f"Imagen con menor calidad: {imagen_menor_blur}")
        progress_bar["value"] = 0
    else:
        printtoconsole("Proceso Detenido")
        stop = False


def select_folder():
    folder_selected = filedialog.askdirectory(title="Seleccionar carpeta de imágenes")
    folder_path.set(folder_selected)
    process_button.config(state="normal")


window = tk.Tk()
window.title("Procesamiento de Imágenes")
window.geometry("580x570")
window.resizable(False, False)
window.iconbitmap("C:/Users/pablo/Downloads/Icono-clasificador.ico")
folder_label = tk.Label(window, text="Carpeta de imágenes:")
folder_label.grid(row=0, column=0, sticky="w")

folder_path = tk.StringVar()
folder_entry = tk.Entry(window, textvariable=folder_path, width=30, state="readonly")
folder_entry.grid(row=0, column=1, sticky="w")

folder_button = tk.Button(window, text="Seleccionar carpeta", command=select_folder)
folder_button.grid(row=0, column=2, padx=5, sticky="w")

set_size_label = tk.Label(window, text="Tamaño del conjunto:")
set_size_label.grid(row=1, column=0, sticky="w")

set_size_var = tk.IntVar()
set_size_combobox = ttk.Combobox(window, textvariable=set_size_var, values=[2, 3, 4, 5, 6, 7, 8, 9, 10], state="readonly")
set_size_combobox.grid(row=1, column=1, sticky="w")
set_size_combobox.set(4)  # Establecer el valor por defecto en 4

kernel_size_label = tk.Label(window, text="Tamaño del filtro:")
kernel_size_label.grid(row=2, column=0, sticky="w")

def validate_filter_size_input(text):
    return text.isdigit() or text == ""

_filter_size_input_command = (window.register(validate_filter_size_input), "%P")

kernel_size_entry = tk.Entry(window, width=5, validate="key", validatecommand=_filter_size_input_command)
kernel_size_entry.insert(tk.END, 20)
kernel_size_entry.grid(row=2, column=1, sticky="w")

process_button = tk.Button(window, text="Procesar Imágenes", command=procesar_imagenes, state=tk.DISABLED)
process_button.grid(row=3, column=2, pady=10, sticky="w")

stop_button = tk.Button(window, text="Detener", command=stop_process, state=tk.DISABLED)
stop_button.grid(row=3, column=1, pady=10, sticky="w")

progress_bar = ttk.Progressbar(window, length=200, mode="determinate")
progress_bar.grid(row=4, column=0, columnspan=2, pady=10)

console_text = tk.Text(window, state="disabled")
console_scrollbar = tk.Scrollbar(window, command=console_text.yview)
console_scrollbar.grid(row=5, column=3, sticky="ns")
console_text.config(yscrollcommand=console_scrollbar.set)
console_text.grid(row=5, column=0, columnspan=3, sticky="nsew")

window.mainloop()
