from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askopenfile
import time

# Refs
# https://pythonguides.com/upload-a-file-in-python-tkinter/

ws = Tk()
ws.title('Face Mask Detector')
ws.geometry('600x200')


def open_file():
    file_path = askopenfile(mode='r', filetypes=[('Image Files', '*jpg')])
    if file_path is not None:
        pass


def uploadFiles():
    pb1 = Progressbar(
        ws,
        orient=HORIZONTAL,
        length=300,
        mode='determinate'
    )
    pb1.grid(row=4, columnspan=3, pady=20)
    for i in range(5):
        ws.update_idletasks()
        pb1['value'] += 20
        time.sleep(1)
    pb1.destroy()
    Label(
        ws,
        text='Picture Uploaded Successfully!',
        foreground='green'
    ).grid(row=4,columnspan=3, pady=10)


adhar = Label(
    ws,
    text='Upload picture with or without a face mask'
)
adhar.grid(row=0, column=0, padx=10)

adharbtn = Button(
    ws,
    text='Choose File',
    command=lambda: open_file()
)
adharbtn.grid(row=0, column=1)

checkForFaceMask = Label(
    ws,
    text='Scan for face mask'
)
checkForFaceMask.grid(row=1, column=0, padx=5)

checkBtn = Button(
    ws,
    text='Start',
    command=uploadFiles
)
checkBtn.grid(row=1, column=1)

def startGUI():
    ws.mainloop()
