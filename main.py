import os
import cv2
import sys
import getopt
import numpy as np
from termcolor import cprint

def getFilePaths():
    opts, args = getopt.getopt(sys.argv[1:], 'p:g:')
    prova = None
    gabarito = None
    for opt, arg in opts:
        if opt == '-p':
            prova = arg
        if opt == '-g':
            gabarito = arg
    return prova, gabarito

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


if __name__ == '__main__':
    pathToProva, pathToGabarito = getFilePaths()
    if pathToProva == None or pathToGabarito == None:
        print('Ambos os paths devem ser fornecidos.')
        pass

    print('Corretor de provas')
    print('O usuario deve passar os paths referentes as pastas das imagens dos gabaritos e depois o arquivo da prova a ser corrigida')

    # load das imagens
    gabaritoImage = cv2.imread(pathToGabarito)
    print('path do gabarito: ', pathToGabarito)
    provaImage = cv2.imread(pathToProva)
    print('path da prova: ', pathToGabarito)

    # thresh_val = 85 # valor semi arbitrário, não  pode ser muito maior pois 
    # binarização é prejudicada caso a imagem tenha sombra, por isso
    # só podemos aceitar até certo ponto de quantidade de sombra
    cv2.imshow('Gabarito Original', gabaritoImage)

    gabaritoAns = getAnswersFromTest(gabaritoImage)
    provaAns = getAnswersFromTest(provaImage)

    print('Respostas obtidas do gabarito: ')
    displayAnswers(provaAns, gabaritoAns)

    cv2.waitKey(0)
    cv2.destroyAllWindows()