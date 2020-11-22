import os
import cv2
import numpy as np

from termcolor import cprint

def getAnswersFromProcessedImage(img, threshold):
    imgColumns = np.array_split(img, 2, axis=1) # split das colunas

    answers = []
    for imgCol in imgColumns:
        options = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E'}
        rows = np.array_split(imgCol, 25)

        for index, row in enumerate(rows):
            rowAnswers = [None] * 5
            columns = np.array_split(row,6,axis=1)
            val = 0
            for i in range(1, 6):
                height, width = columns[i].shape
                val = height * width # contagem de pixels na celula
                rowAnswers[i - 1] = np.count_nonzero(columns[i])
            
            # seleciona se há uma marcação clara em cada célula da questão
            answered = [(item / (val/3.5)) > threshold for item in rowAnswers]
            if sum(answered) == 1:
                answers.append(options[answered.index(True)])
            else:
                answers.append(None)

    return answers

def getAnswersFromTest(img):
    # img = cv2.imread(path)
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgThreshold = cv2.threshold(imgGray, 85, 255, cv2.THRESH_BINARY_INV)[1]
    cv2.imshow('img com thresh', imgThreshold)
    return getAnswersFromProcessedImage(imgThreshold, 0.5)

def displayAnswers(listaProva, listaGabarito):
    right_ans = 0
    print('Respostas:     Prova       Gabarito')
    for i in range(len(listaProva)):
        if(listaProva[i] != None and listaProva[i] == listaGabarito[i]):
            cprint("Questao " + str(i + 1) + ":      " + str(listaProva[i])+ '       ' + str(listaGabarito[i]), 'green')
            right_ans += 1
        else:
            cprint("Questao " + str(i + 1) + ":      " + str(listaProva[i])+ '       ' + str(listaGabarito[i]), 'red')
    print('')
    print('Respostas certas: ', right_ans)

# parametro da função é o path do diretório com as imagens do gabaritos
def organizarPastaGabaritos(imagesPaths):
    lista_files = os.listdir(imagesPaths)
    tiposGabaritos = {}
    for gabaritoPath in lista_files:
        tipo = gabaritoPath.split('.')[0].split('_')[-1] # pega o numero que serve idenetificador do tipo
        if(imagesPaths[-1] == '/'):
            pathCompletoGabarito = imagesPaths + gabaritoPath
        else:
            pathCompletoGabarito = imagesPaths + '/' + gabaritoPath
        tiposGabaritos[tipo] = pathCompletoGabarito
    return tiposGabaritos