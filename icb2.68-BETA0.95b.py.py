# Copyright (C) 2023 Frank IUØESP
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# importazione delle librerie necessarie per il funzionamento del programma
import tkinter as tk
import serial
import webbrowser
import serial.tools.list_ports
import random
from PIL import Image, ImageTk
import requests
from io import BytesIO

# dichiarazione della variabile bool random_toggle_active
random_toggle_active = False


def download_image(url):
    response = requests.get(url)
    if response.status_code == 200:
        return Image.open(BytesIO(response.content))
    else:
        return None


# Definizione della funzione toggle_rts()
def toggle_rts():
    if 'ser' in globals():
        ser.setRTS(not ser.rts)
        if ser.rts:
            canvas.itemconfig(rts_led, fill="#FFD700", outline="white")
        else:
            canvas.itemconfig(rts_led, fill="white")


# Definizione della funzione toggle_dtr()
def toggle_dtr():
    if 'ser' in globals():
        ser.setDTR(not ser.dtr)
        if ser.dtr:
            canvas.itemconfig(dtr_led, fill="blue", outline="white")
        else:
            canvas.itemconfig(dtr_led, fill="white")


# Definizione della funzione set_com_port()
def set_com_port(com_num):
    global ser
    port = f'COM{com_num}'
    if port in available_ports():
        ser = serial.Serial(port, timeout=1)
        ser.setDTR(False)
        ser.setRTS(False)
        canvas.itemconfig(dtr_led, fill="white")
        canvas.itemconfig(rts_led, fill="white")
        status_label.config(text=f"{port} found!", fg="green")  # trovo la porta metto il verde per averla trovata
    else:
        ser = None
        status_label.config(text="COM not found", fg="red")  # non trovo la porta metto il rosso per non averla trovata


# Definizione della funzione available_ports()
def available_ports():
    ports = []
    for port, desc, hwid in serial.tools.list_ports.comports():
        ports.append(port)
    return ports


# Definizione della funzione apri_link()
# def apri_link(event):
#    webbrowser.open("https://www.qrzcb.io/icb")  # Link al sito web principale

# Definizione della funzione open_url(event)
def open_url(event):
    webbrowser.open_new('https://www.qrzcb.io')  # https è molto più sicuro, apro il sito in una nuova finestra


# Definzione della funzione random_toggle()
def random_toggle():
    global random_toggle_active
    random_toggle_active = not random_toggle_active
    do_random_toggle()


# Definizione della funzione do_random_toggle()
def do_random_toggle():
    global random_toggle_active
    if random_toggle_active:
        if 'ser' in globals():
            random_rts = random.choice([True, False])
            random_dtr = random.choice([True, False])

            ser.setRTS(random_rts)
            ser.setDTR(random_dtr)

            if random_rts:
                canvas.itemconfig(rts_led, fill="#FFD700", outline="white")
            else:
                canvas.itemconfig(rts_led, fill="white")

            if random_dtr:
                canvas.itemconfig(dtr_led, fill="blue", outline="white")
            else:
                canvas.itemconfig(dtr_led, fill="white")

            random_status.config(text="ON", fg="green")  # Aggiorna il testo della label con ON di colore verde
        else:
            random_status.config(text="OFF", fg="red")  # Aggiorna il testo della label con OFF di colore rosso

    root.after(500, do_random_toggle)


# Inizializzo la finestra contenente il tutto
root = tk.Tk()
# Imposto il titolo
root.title('QRZCB.io - Test Pin RTS & DTR Com Port - V0.80 - QRZCB.io')
root.grid()  # Setto l'autodimensionamento della finestra con grid()
root.resizable(False, False)  # E' un booleano se non vuoi fare il ridimensionamento devi mettere entrambi a false
root.config(bg="#111111")  # Imposto la finestra con questo codice colore

# Imposto il titolo del programma
title_label = tk.Label(root, bg="#111111", fg="white", text='iCB-TEST v0.9b', font=('Arial', 20))
title_label.pack()

# Imposto il collegamento al sito principale
new_label = tk.Label(root, bg="#111111", text='https://www.qrzcb.io',
                     font=('Arial', 13, 'bold'), fg='#29d9d5', cursor='hand2')
new_label.bind("<Button-1>", open_url)
new_label.pack()

# Imposto la scritta dell'autore del programma
new_label = tk.Label(root, bg="#111111", text='written by Frank IUØESP',
                     font=('Arial', 11, 'bold'), fg='white')
new_label.pack(pady=10)

# Imposto un link alle istruzioni della scheda sul sito
# new_label = tk.Label(root, bg="#111111", text='Clicca qui per visitare il sito',
#                    font=('Arial', 11, 'bold'), fg='#29d9d5', cursor='hand2')
# new_label.bind("<Button-1>", apri_link)
# new_label.pack(pady=10)


# imposto il frame contenente le porte com da selezionare
com_frame = tk.Frame(root, bg="#111111")
com_frame.pack(pady=1)

# imposto il valore a 1 per la porta selezionata
com_num = tk.StringVar(value='1')

# Faccio 2 cicli per settare le porte com dalla 1 alla 7 e dalla 7 alla 13
for i in range(1, 7):
    tk.Radiobutton(com_frame, bg="#111111", fg="#29d9d5", text=f"COM{i}", variable=com_num, value=f"{i}",
                   command=lambda i=i: set_com_port(i)).grid(row=0, column=i - 1)
for i in range(7, 13):
    tk.Radiobutton(com_frame, bg="#111111", fg="#29d9d5", text=f"COM{i}", variable=com_num, value=f"{i}",
                   command=lambda i=i: set_com_port(i)).grid(row=1, column=i - 7)

# Imposto uno status che indica la scelta della porta
status_label = tk.Label(root, bg="#111111", fg="yellow", text="Choose COM port !", font=('Arial', 16))
status_label.pack(pady=10)

# Imposto una finestra interna contenente l'immaggine con i led RTS e DTR
canvas = tk.Canvas(root, width=300, height=200, bg="#111111")
canvas.pack(pady=10)

# Importo l'immagine nella finestra di cui sopra
# image_path = "D:\\Documenti\\ProgettiFrank\\iCBEasyInterfaceIU0ESPprogrammaTestSchedaBeta\\interface3d.png"
image_url = "https://www.qrzcb.io/dv/interface3d.png"
image = download_image(image_url)
# img = Image.open(image_url)
pcb_image = ImageTk.PhotoImage(image)
canvas.create_image(0, 0, anchor="nw", image=pcb_image)
# canvas.create_image(30, 20, anchor="nw", image=pcb_image) # aumentato di 30 per la posizione dell'immagine

# Imposto manualmente le coordinate per i led
rts_led = canvas.create_oval(178, 61, 192, 76, fill="white")
# rts_led = canvas.create_oval(208, 81, 222, 96, fill="white") # aumentato di 30 per la posizione dell'immagine
dtr_led = canvas.create_oval(172, 97, 187, 112, fill="white")
# dtr_led = canvas.create_oval(202, 117, 217, 132, fill="white") # aumentato di 30 per la posizione dell'immagine

# Imposto un nuovo frame per i pulsanti Change RTS e Change DTR
button_frame = tk.Frame(root, bg="#111111")
button_frame.pack(pady=10)

# Imposto il bottone RTS
rts_button = tk.Button(button_frame, bg="#111111", fg="#29d9d5", text="Change RTS",
                       command=toggle_rts, font=('Arial', 15))
rts_button.grid(row=0, column=1, padx=10, pady=10)

# Imposto il bottone DTR
dtr_button = tk.Button(button_frame, bg="#111111", fg="#29d9d5", text="Change DTR",
                       command=toggle_dtr, font=('Arial', 15))
dtr_button.grid(row=0, column=2, padx=10, pady=10)

# Imposto il Frame per il bottone random
random_frame = tk.Frame(button_frame, bg="#111111")
random_frame.grid(row=1, column=1, padx=10, pady=10)

# Imposto un testo per il random
# random_label = tk.Label(random_frame, bg="#111111", fg="#29d9d5", text="Random Test:", font=('Arial', 12))
# random_label.pack(side=tk.LEFT)

# Imposto il bottone per il test random
random_button = tk.Button(random_frame, bg="#111111", fg="#29d9d5", text="Random",
                          command=random_toggle, font=('Arial', 12))
random_button.pack()

# Imposto il testo per lo status random OFF o ON
random_status = tk.Label(button_frame, bg="#111111", text="OFF", font=('Arial', 12), fg="red")
random_status.grid(row=1, column=1, columnspan=10)

# Imposto il bottone Chiudi per chiudere il programma
close_button = tk.Button(button_frame, bg="#111111", fg="#29d9d5", text="Chiudi", command=root.quit, font=('Arial', 15))
close_button.grid(row=1, column=2, columnspan=10)

# Loop della finestra del programma
root.mainloop()

# Controllo della variabile ser in caso di errore chiude il programma
if 'ser' in globals():
    ser.close()
