import cv2
import numpy as np
img = cv2.imread('imagens/gabaritos/gabarito_1.jpeg')

imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgThreshold = cv2.threshold(imgGray, 85, 255, cv2.THRESH_BINARY_INV)[1]

cv2.imshow('gabarito', imgThreshold)

majorCols = np.array_split(imgThreshold, 2, axis=1)

cv2.imwrite('primeira_colunas.png',majorCols[0])
cv2.imwrite('segunda_colunas.png',majorCols[1])

questArray = np.array_split(majorCols[0], 25)
cv2.imwrite('quest_11.png', questArray[10])

questao_11 = np.array_split(questArray[10], 6, axis=1)
cv2.imshow('A da 11',questao_11[1])
cv2.imwrite('questao_11_a.png', questao_11[1])
cv2.imshow('B da 11',questao_11[2])
cv2.imwrite('questao_11_B.png', questao_11[2])
# for col in majorCols:
#     for i in range(len(questArray)):
#         if(i == 10):
#             cv2.imwrite('quest_11.png', questArray[i])

        # alternativas = np.array_split(question, 6, axis=1)
        # for cell in alternativas:

# cv2.imwrite('binarizada.png', imgThreshold)

cv2.waitKey(0)
cv2.destroyAllWindows()