import tkinter as tk
import serial
import webbrowser
import serial.tools.list_ports
import random

random_toggle_active = False

def toggle_rts():
    if 'ser' in globals():
        ser.setRTS(not ser.rts)
        if ser.rts:
            canvas.itemconfig(rts_led, fill="#FFD700", outline="white")
        else:
            canvas.itemconfig(rts_led, fill="white")

def toggle_dtr():
    if 'ser' in globals():
        ser.setDTR(not ser.dtr)
        if ser.dtr:
            canvas.itemconfig(dtr_led, fill="blue", outline="white")
        else:
            canvas.itemconfig(dtr_led, fill="white")

def set_com_port(com_num):
    global ser
    port = f'COM{com_num}'
    if port in available_ports():
        ser = serial.Serial(port, timeout=1)
        ser.setDTR(False)
        ser.setRTS(False)
        canvas.itemconfig(dtr_led, fill="white")
        canvas.itemconfig(rts_led, fill="white")
        status_label.config(text=f"{port} found!", fg="green")
    else:
        ser = None
        status_label.config(text="COM not found", fg="red")

def available_ports():
    ports = []
    for port, desc, hwid in serial.tools.list_ports.comports():
        ports.append(port)
    return ports

def open_url(event):
    webbrowser.open_new('http://www.qrzcb.io')

def random_toggle():
    global random_toggle_active
    random_toggle_active = not random_toggle_active
    do_random_toggle()


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

            random_status.config(text="ON", fg="green")  # Aggiorna il testo della label
        else:
            random_status.config(text="OFF", fg="red")  # Aggiorna il testo della label

    root.after(500, do_random_toggle)



root = tk.Tk()
root.title('QRZCB.io - Test Pin RTS & DTR Com Port - V0.80 - QRZCB.io')
root.geometry('900x600')
root.resizable(0, 0)

title_label = tk.Label(root, text='CQ CQ!!! Easy TEST DTR&RTS', font=('Arial', 20))
title_label.pack(pady=10)

new_label = tk.Label(root, text='written by Frank IU0ESP', font=('Arial', 8, 'bold'), fg='blue', cursor='hand2')
new_label.bind("<Button-1>", open_url)
new_label.pack(pady=10)

com_frame = tk.Frame(root)
com_frame.pack(pady=1)

com_num = tk.StringVar(value='1')

for i in range(1, 7):  
    tk.Radiobutton(com_frame, text=f"COM{i}", variable=com_num, value=f"{i}", command=lambda i=i: set_com_port(i)).grid(row=0, column=i-1)
for i in range(7, 13):  
    tk.Radiobutton(com_frame, text=f"COM{i}", variable=com_num, value=f"{i}", command=lambda i=i: set_com_port(i)).grid(row=1, column=i-7)

canvas = tk.Canvas(root, width=300, height=200)
canvas.pack()

pcb_image = tk.PhotoImage(file="interface3d.gif")
canvas.create_image(0, 0, anchor="nw", image=pcb_image)

rts_led = canvas.create_oval(178, 61, 192, 76, fill="white")
dtr_led = canvas.create_oval(172, 97, 187, 112, fill="white")

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

rts_button = tk.Button(button_frame, text="Change RTS", command=toggle_rts, font=('Arial', 15))
rts_button.grid(row=0, column=0, padx=10, pady=10)

dtr_button = tk.Button(button_frame, text="Change DTR", command=toggle_dtr, font=('Arial', 15))
dtr_button.grid(row=0, column=1, padx=10, pady=10)

random_frame = tk.Frame(button_frame)
random_frame.grid(row=0, column=2, padx=10, pady=10)

random_label = tk.Label(random_frame, text="Random Test:", font=('Arial', 12))
random_label.pack(side=tk.LEFT)

random_status = tk.Label(random_frame, text="OFF", font=('Arial', 12), fg="red")
random_status.pack(side=tk.LEFT)

random_button = tk.Button(random_frame, text="Toggle", command=random_toggle, font=('Arial', 12))
random_button.pack(side=tk.LEFT)

status_label = tk.Label(root, text="", font=('Arial', 16))
status_label.pack(pady=10)

close_button = tk.Button(root, text="Chiudi", command=root.quit, font=('Arial', 15))
close_button.pack(pady=10)

root.mainloop()

if 'ser' in globals():
    ser.close()
