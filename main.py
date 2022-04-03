# This is a sample Python script.
import random
from tkinter import messagebox
import tkinter as tk

def getIndexesToXor(array):
    result = []
    for idx, val in enumerate(array):
        if(val == 1):
            result.append(idx)
    return result

def lsfrCycle():
    mask = 0
    try:
        mask = int(textTF.get())
    except ValueError:
        return 0
    cycleLimit = 2**len(str(mask)) - 1
    result = []
    block = []
    print(str(mask))
    for element_in_mask in range(len(str(mask))):
        block.append(random.randint(0, 1))
    array = getIndexesToXor([int(y) for y in str(mask)])
    for i in range(cycleLimit):
        result.append(int(block[-1]))
        value = None
        for idx in array:
            if value is None:
                value = block[idx]
            else:
                value = bool(value) ^ bool(block[idx])
        tmp = None
        tmp2 = None
        for idx, val in enumerate(block):
            if idx == 0:
                tmp = block[idx]
                block[idx] = value
            elif idx < len(block):
                tmp2 = block[idx]
                block[idx] = tmp
                tmp = tmp2
    return result

def lfsrFun():
    if(sposob.get() == 0):
        messagebox.showerror("Nie wybrano sposobu!")
    elif(sposob.get() == 2):
        result = lsfrCycle()
        strResult = ''.join([str(elem) for elem in result])
        messagebox.showinfo("Wynik", "Wygenerowany LFSR: {}".format(strResult))

master = tk.Tk()
sposob = tk.IntVar()

header = tk.Label(master, text="GENERATORY LICZB PSEUDOLOSOWYCH. \n SZYFRY STRUMIENIOWE", font="Helvetica 16 bold italic").grid(row=0, columnspan=2)

textLabel = tk.Label(master, text="Podaj wielomian:").grid(row=1)
textTF = tk.Entry(master, width=50)
textTF.grid(row=1,column=1,columnspan=3)
examplePolynomialsLabel = tk.Label(master, text="Przykład: Jeżeli chce się podać wielomian \n 𝜑(𝑥) = 1 + 𝑥 + 𝑥^4\n Podaj odpowiadające potegi: 11001", font="Helvetica 10 italic").grid(row=2,column=1, columnspan=3)
emptyLabel = tk.Label(master).grid(row=3,columnspan=4,rowspan=3)
sposobRadioLabel = tk.Label(master, text="Sposób działania generatora liczb pseudolosowych:").grid(row=5, column=0,rowspan=3)
R1 = tk.Radiobutton (master, text="W nieskonczonosc, do momentu wcisniecia Spacji", variable=sposob, value=1)
R1.grid(row=6,column=1, padx=0)
R2 = tk.Radiobutton (master, text="Do wykrycia cyklu", variable=sposob, value=2)
R2.grid(row=7,column=1, padx=0)

LFSRButton = tk.Button(master, text="GENERATOR LICZB PSEUDOLOSOWYCH", command=lfsrFun).grid(row=8,column=0)
master.geometry("800x600")
master.mainloop()

