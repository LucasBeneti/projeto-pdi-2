import cv2
import numpy as np

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

def compareAnswersAndGetScore(gabarito, prova):
    score = 0
    for i in range(0, 50):
        g = gabarito[i]
        p = prova[i]
        if g == None:
            continue
        if g == p:
            score += 1
    return score

def displayAnswers(listaProva, listaGabarito):
    print('Respostas:     Prova       Gabarito')
    for i in range(len(listaProva)):

        print("Questao " + str(i + 1) + ":      " + str(listaProva[i])+ '       ' + str(listaGabarito[i]))
    print('')

# prova = getAnswersFromTest("imagens/prova_1.jpeg")
# gabarito = getAnswersFromTest("imagens/gabarito_1.jpeg")
# print('gabarito ',gabarito)
# score = compareAnswersAndGetScore(gabarito, prova)

# print("Nota: " + str(score))