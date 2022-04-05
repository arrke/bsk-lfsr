# This is a sample Python script.
import random
from tkinter import messagebox
import tkinter as tk
import bitarray
from tkinter import filedialog as fd

filename = 0

def getIndexesToXor(array):
    result = []
    for idx, val in enumerate(array):
        if(val == 1):
            result.append(idx)
    return result

def lsfr(version):
    mask = 0
    try:
        mask = int(textTF.get())
    except ValueError:
        messagebox.showerror("MASKA", "Nie poprawna maska")
        return 0
    cycleLimit = 0
    blockLen = 0
    if version is None:
        cycleLimit = 2**len(str(mask)) - 1
        blockLen = len(str(mask))
    else:
        cycleLimit = len(version)
        blockLen = len(version)
    result = []
    block = []
    print(str(mask))
    seed = ''
    if seedTF.get() != '':
        try:
            seed = int(seedTF.get())
            if len(str(seed)) < len(str(mask)):
                messagebox.showerror("SEED", "seed nie ma tej samej dlugosci co maska")
                return
        except ValueError:
            messagebox.showerror("SEED", "Seed niepoprawny")
            return 0

    if seed != '':
        block = [int(y) for y in list(str(seed))]
    else:
        for element_in_mask in range(blockLen):
            block.append(random.randint(0, 1))
    print(block)
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
    result = lsfr(None)
    if result == 0:
        return
    strResult = ''.join([str(elem) for elem in result])
    messagebox.showinfo("Wynik", "Wygenerowany LFSR: {}".format(strResult))

def ssc():
    ba = bitarray.bitarray()
    text = nameTF.get()
    if text == '':
        messagebox.showerror("BRAK NAZWY", "NIE PODANO NAZWY DO SZYFROWANIA")
        return
    ba.frombytes(text.encode("utf-16"))
    print("KOD")
    print(''.join([str(y) for y in ba.tolist()]))
    textbytes = ba.tolist().copy()
    resultlsfr = lsfr(ba)
    if resultlsfr == 0:
        return
    result = []
    for i in range(len(textbytes)):
        result.append(resultlsfr[i] ^ textbytes[i])
    messagebox.showinfo("Wynik", "Zaszyfrowany ciąg: {}".format(bitarray.bitarray(result).tobytes().decode("utf-16")))

def ssc_with_file():
    global filename
    ba = bitarray.bitarray()
    if filename == 0:
        messagebox.showerror("BRAK PLIKU", "NIE PODANO PLIKU DO SZYFROWANIA")
        return
    file = open(filename, 'rb')
    data = file.read()
    ba.frombytes(data)
    textbytes = ba.tolist().copy()
    resultlsfr = lsfr(ba)
    if resultlsfr == 0:
        return
    result = []
    for i in range(len(textbytes)):
        result.append(resultlsfr[i] ^ textbytes[i])
    messagebox.showinfo("Wynik",
                        "Zaszyfrowany ciąg: {}".format(bitarray.bitarray(result).tobytes().decode("ISO-8859-1")))


def addFile():
    global filename
    filename = fd.askopenfilename()
    messagebox.showinfo(title="Dodano plik", message=filename)
    fileNameLabel.config(text = filename)

master = tk.Tk()

header = tk.Label(master, text="GENERATORY LICZB PSEUDOLOSOWYCH. "
                               "\n SZYFRY STRUMIENIOWE", font="Helvetica 16 bold italic")   .grid(row=0, columnspan=2)

textLabel = tk.Label(master, text="Podaj wielomian:").grid(row=1)
textTF = tk.Entry(master, width=50)
textTF.grid(row=1,column=1,columnspan=3)
examplePolynomialsLabel = tk.Label(master, text="Przykład: Jeżeli chce się podać wielomian"
                                                " \n f(x) = 1 + x + x^4\n Podaj odpowiadające potegi: 11001",
                                   font="Helvetica 10 italic").grid(row=2,column=1, columnspan=3)
emptyLabel = tk.Label(master).grid(row=3,columnspan=4,rowspan=3)

seedLabel = tk.Label(master, text="Podaj seed poczatkowy").grid(row=4,column=0)
seedTF = tk.Entry(master, width=50)
seedTF.grid(row=4, column=1)

nameLabel = tk.Label(master, text="Podaj text do zaszyfrowania").grid(row=5, column=0)
nameTF = tk.Entry(master, width=50)
nameTF.grid(row=5, column=1)
fileButton = tk.Button(master, text="Dodaj plik", command=addFile)
fileButton.grid(row=6, column=0)
fileNameLabel = tk.Label(master, text="")
fileNameLabel.grid(row=6, column=1)
LFSRButton = tk.Button(master, text="GENERATOR LICZB PSEUDOLOSOWYCH", command=lfsrFun).grid(row=8,column=0)
SSCButton = tk.Button(master, text="SZYFR STRUMIENIOWY", command=ssc).grid(row=8, column = 1)
SSCButton = tk.Button(master, text="SZYFR STRUMIENIOWY Z PLIKIEM", command=ssc_with_file).grid(row=8, column = 2)

master.geometry("800x600")
master.mainloop()

